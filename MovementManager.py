"""
MovementManager.py

Handles paddle movement for human players and a difficulty-scaled predictive AI opponent.
- Player controls (left/right paddles) via configurable key maps.
- AI paddle predicts ball trajectory for interception, with smoothing.
- AI behavior parameters (speed, gain, dead zone) scale with difficulty level 1-3.
- Constrains paddle within screen bounds.
"""

import sys
import pygame
import GlobalData
from constants import gWidth, gHeight, REFRESH


class MovementManager:
    """Static class managing player and AI paddle movements."""

    # Human paddle movement speed (pixels per frame)
    sprite_speed: int = 25

    # Key mappings for player control: key -> direction multipler
    key_map_left = {pygame.K_w: -1, pygame.K_s: 1}
    key_map_right = {pygame.K_UP: -1, pygame.K_DOWN: 1}

    @staticmethod
    def _constrain_y(y: float, paddle_height: int) -> float:
        """
        Constrain Y-position so paddle stays within screen boundaries.
        """
        if y < 0:
            return 0
        max_y = gHeight - paddle_height
        return max(0, min(y, max_y))

    @staticmethod
    def _move_player(event: pygame.event.Event, paddle, key_map):
        """
        Move given paddle based on a KEYDOWN event and mapping.
        """
        direction = key_map.get(event.key)
        if direction is None:
            return
        x, y = paddle.get_pos()
        dy = direction * MovementManager.sprite_speed
        new_y = MovementManager._constrain_y(y + dy, paddle.get_height())
        paddle.update_loc(x, new_y)

    @staticmethod
    def _predict_ball_intercept(ball):
        """
        Predict the future Y position of the ball when it reaches the AI paddle's X.
        Accounts for wall bounces.
        """
        bx, by = ball.get_pos()
        dx, dy = ball.get_move()
        # Default center if ball moving away
        # If ball moving away, track its current position to return paddle towards ball
        if dx <= 0:
            return by + ball.get_height() / 2
        # AI paddle x-coordinate
        _, ai_paddle = GlobalData.sprite_list.sprites()
        paddle_x = ai_paddle.get_pos()[0]
        distance_x = paddle_x - bx
        time_to_reach = distance_x / dx
        predicted_y = by + dy * time_to_reach
        # Simulate vertical reflections
        period = 2 * (gHeight - ball.get_height())
        mod_y = predicted_y % period
        if mod_y > (gHeight - ball.get_height()):
            mod_y = period - mod_y
        return mod_y + ball.get_height() / 2

    @staticmethod
    def _ai_parameters():
        """
        Return AI parameters (kp, dead_zone, speed) based on difficulty level 1-3.
        Higher level => higher gain, smaller dead zone, faster paddle.
        """
        level = getattr(GlobalData, 'com_level', 1)
        level = max(1, min(level, 3))
        # Base parameters
        base_kp = 0.5
        base_dead = 20
        # Scale per level
        kp = base_kp + 0.25 * (level - 1)
        dead_zone = base_dead - 5 * (level - 1)
        speed = MovementManager.sprite_speed + 5 * (level - 1)
        return kp, dead_zone, speed

    @staticmethod
    def _move_ai(paddle, target_y_center):
        """
        Move AI paddle's center toward target_y_center using scaled parameters.
        Ensures minimum movement to avoid stagnation.
        """
        x, y = paddle.get_pos()
        paddle_center = y + paddle.get_height() / 2
        error = target_y_center - paddle_center
        kp, dead_zone, speed = MovementManager._ai_parameters()
        if abs(error) < dead_zone:
            return
        # Proportional step
        step = kp * error
        # Ensure at least 1 pixel movement
        if abs(step) < 1:
            step = 1 if step > 0 else -1
        # Clamp step by speed
        step = max(-speed, min(speed, step))
        new_y = MovementManager._constrain_y(y + step, paddle.get_height())
        paddle.update_loc(x, new_y)

    @staticmethod
    def sprite_movement(event: pygame.event.Event = None):
        """
        Dispatch movement for human players and AI each frame.
        AI parameters adjust by GlobalData.com_level (1=easy,3=hard).
        """
        left_paddle, right_paddle = GlobalData.sprite_list.sprites()

        # Handle human moves
        if event and event.type == pygame.KEYDOWN:
            MovementManager._move_player(event, left_paddle,
                                          MovementManager.key_map_left)
            if not GlobalData.against_com:
                MovementManager._move_player(event, right_paddle,
                                              MovementManager.key_map_right)

        # AI movement
        if GlobalData.against_com:
            balls = GlobalData.ball_list.sprites()
            if not balls:
                return
            target_y = MovementManager._predict_ball_intercept(balls[0])
            MovementManager._move_ai(right_paddle, target_y)

    @staticmethod
    def game_loop_movement(clock: pygame.time.Clock):
        """
        Continuous AI updater (no event) with scaled difficulty.
        """
        if GlobalData.against_com:
            left_paddle, right_paddle = GlobalData.sprite_list.sprites()
            balls = GlobalData.ball_list.sprites()
            if balls:
                target_y = MovementManager._predict_ball_intercept(balls[0])
                MovementManager._move_ai(right_paddle, target_y)
        clock.tick(REFRESH)

"""
CollisionManager.py

Handles collisions for Pong game:
- Paddle collisions (with reflection and speed increase)
- Wall collisions (top/bottom bounce)
- Side collisions (scoring and respawn)
- Game over detection and restart flow
- Utility for centering ball and checking overlap
"""

import sys
import random
import pygame
import GlobalData
from constants import gWidth, gHeight, BallSpeedPix, AddSpeedBall, Xdeviation, REFRESH
from GameTextManager import GameTextManager


class CollisionManager:
    """Static class for collision logic and game-over handling."""

    @staticmethod
    def handle_paddle_collision(ball, left_paddle, right_paddle,
                                x_move, paddle_w, paddle_h,
                                sound_effect, y_speeds, play_sound):
        """
        Check collision with paddles and compute new velocity.

        Returns:
            (new_x, new_y) if collision occurred, else None.
        """
        x_ball, y_ball = ball.get_pos()
        for paddle, side in ((right_paddle, 'r'), (left_paddle, 'l')):
            if CollisionManager._check_overlap(
                    x_ball, y_ball,
                    *paddle.get_pos(), paddle_w, paddle_h,
                    side, y_ball + ball.get_height()
                ):
                play_sound(sound_effect)
                direction = -1 if side == 'r' else 1
                new_x = direction * abs(x_move) + direction * AddSpeedBall
                new_y = random.choice(y_speeds)
                return new_x, new_y
        return None

    @staticmethod
    def handle_wall_collision(y_ball, y_move, ball_height):
        """
        Bounce ball off top/bottom walls.

        Returns new_y velocity or None if no collision.
        """
        if y_ball <= 0:
            return abs(y_move)
        if y_ball >= gHeight - ball_height:
            return -abs(y_move)
        return None

    @staticmethod
    def handle_side_collision(ball, index, x_ball, sound_list):
        """
        Handle scoring when ball crosses left/right boundary.

        Plays sound, respawns ball at center, updates lives,
        and triggers game-over if needed.

        Returns:
            (new_x, new_y) new velocity after respawn.
        """
        CollisionManager._play_sound(sound_list[1])

        # Random direction respawn
        new_x = random.choice([-BallSpeedPix, BallSpeedPix])
        new_y = random.choice([-BallSpeedPix, BallSpeedPix])

        ball.update_Move(new_x, new_y)
        CollisionManager._center_ball(index)

        # Decrement life
        paddles = GlobalData.sprite_list.sprites()
        if x_ball <= 0:
            paddles[0].lose_life('left')
        else:
            paddles[1].lose_life('right')

        CollisionManager._check_game_over()
        return new_x, new_y

    @staticmethod
    def _check_game_over():
        """
        Check lives and display game-over screen if zero.
        """
        paddles = GlobalData.sprite_list.sprites()
        left_life = paddles[0].get_life()[0]
        right_life = paddles[1].get_life()[1]

        if left_life <= 0:
            GameTextManager.game_over_message(
                'Computer' if GlobalData.against_com else 'Right'
            )
            CollisionManager._wait_for_restart()
        elif right_life <= 0:
            GameTextManager.game_over_message('Left')
            CollisionManager._wait_for_restart()

    @staticmethod
    def _wait_for_restart():
        """
        Pause game flow until user presses a key to restart or quit.
        """
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    from pongGame import start_game  # avoid circular import
                    start_game()
            clock.tick(REFRESH)

    @staticmethod
    def _center_ball(index):
        """
        Move specified ball to center of the screen.
        """
        ball = GlobalData.ball_list.sprites()[index]
        center_x = gWidth / 2 - ball.get_width() / 2
        center_y = gHeight / 2 - ball.get_height() / 2
        ball.update_loc(center_x, center_y)

    @staticmethod
    def _check_overlap(x_ball, y_ball, x_pad, y_pad,
                       pad_w, pad_h, side, y_ball_bottom):
        """
        Return True if ball overlaps paddle in correct region.
        """
        # Vertical overlap
        if y_ball_bottom < y_pad or y_ball > y_pad + pad_h:
            return False
        # Horizontal check based on side
        if side == 'r':
            return x_ball >= x_pad - Xdeviation - pad_w
        else:
            return x_ball <= x_pad + Xdeviation

    @staticmethod
    def _play_sound(sound):
        """
        Play sound on available mixer channel.
        """
        channel = pygame.mixer.find_channel()
        if channel:
            channel.queue(sound)

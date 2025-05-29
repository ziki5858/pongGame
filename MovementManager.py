
import random
from constantsGlobal import *


class MovementManager:
    """Static class managing player and AI paddle movements with multi-ball support and difficulty scaling."""

    sprite_speed: int = 25  # Human paddle movement speed
    key_map_left = {pygame.K_w: -1, pygame.K_s: 1}
    key_map_right = {pygame.K_UP: -1, pygame.K_DOWN: 1}

    @staticmethod
    def _constrain_y(y: float, paddle_height: int) -> float:
        """Ensure paddle stays within vertical bounds."""
        return max(0, min(y, gHeight - paddle_height))

    @staticmethod
    def _move_player(event, paddle, key_map):
        """Move paddle based on a KEYDOWN event."""
        direction = key_map.get(event.key)
        if direction is None:
            return
        x, y = paddle.get_pos()
        dy = direction * MovementManager.sprite_speed
        new_y = MovementManager._constrain_y(y + dy, paddle.get_height())
        paddle.update_loc(x, new_y)

    @staticmethod
    def _predict_ball_intercept(ball):
        """Predict Y position and time for ball to reach AI paddle's X coordinate."""
        bx, by = ball.get_pos()
        dx, dy = ball.get_move()
        # If ball moving away, ignore
        if dx <= 0:
            return None, float('inf')
        _, ai_paddle = GlobalData.sprite_list.sprites()
        paddle_x = ai_paddle.get_pos()[0]
        time_to_hit = (paddle_x - bx) / dx
        pred_y = by + dy * time_to_hit
        # reflect on walls
        period = 2 * (gHeight - ball.get_height())
        mod = pred_y % period
        if mod > (gHeight - ball.get_height()):
            mod = period - mod
        return mod + ball.get_height() / 2, time_to_hit

    @staticmethod
    def _move_ai(paddle, target_y):
        """Move AI paddle toward target Y with difficulty-based smoothing and speed."""
        if target_y is None:
            return
        x, y = paddle.get_pos()
        h = paddle.get_height()
        center = y + h / 2
        error = target_y - center
        level = max(1, min(getattr(GlobalData, 'com_level', 1), 3))
        # settings per level: (alpha, max_speed, dead_zone, skip_chance)
        settings = {
            1: (0.02, 1, 100, 0.6),
            2: (0.1, 4, 50, 0.2),
            3: (0.2, 8, 20, 0.0),
        }[level]
        alpha, max_speed, dead_zone, skip = settings
        # random skip for mistakes
        if random.random() < skip:
            return
        if abs(error) <= dead_zone:
            return
        step = alpha * error
        step = max(-max_speed, min(max_speed, step))
        new_y = MovementManager._constrain_y(y + step, h)
        paddle.update_loc(x, new_y)

    @staticmethod
    def sprite_movement(event=None):
        """Handle human and AI movements each frame."""
        paddles = GlobalData.sprite_list.sprites()
        if len(paddles) < 2:
            return
        left_paddle, right_paddle = paddles
        # Human movement
        if event and event.type == pygame.KEYDOWN:
            MovementManager._move_player(event, left_paddle, MovementManager.key_map_left)
            if not GlobalData.against_com:
                MovementManager._move_player(event, right_paddle, MovementManager.key_map_right)
        # AI movement
        if GlobalData.against_com:
            best_target, best_time = None, float('inf')
            for ball in GlobalData.ball_list.sprites():
                pred, t = MovementManager._predict_ball_intercept(ball)
                if 0 <= t < best_time:
                    best_time, best_target = t, pred
            if best_target is not None:
                MovementManager._move_ai(right_paddle, best_target)

    @staticmethod
    def game_loop_movement(clock):
        """Continuous AI updates without events."""
        if GlobalData.against_com:
            paddles = GlobalData.sprite_list.sprites()
            if len(paddles) < 2:
                return
            _, right_paddle = paddles
            best_target, best_time = None, float('inf')
            for ball in GlobalData.ball_list.sprites():
                pred, t = MovementManager._predict_ball_intercept(ball)
                if 0 <= t < best_time:
                    best_time, best_target = t, pred
            if best_target is not None:
                MovementManager._move_ai(right_paddle, best_target)
        clock.tick(REFRESH)

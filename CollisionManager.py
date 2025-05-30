import sys, random, pygame
from constantsGlobal import (
    gWidth, gHeight, Xdeviation, BallSpeedPix,
    GlobalData, REFRESH
)
from GameTextManager import GameTextManager


class CollisionManager:
    """Pure-logic helpers for paddle / wall / side collisions."""

    # =========================================================
    #  PUBLIC STATIC METHODS
    # =========================================================
    @staticmethod
    def handle_paddle_collision(ball, left_pad, right_pad,
                                vx, pad_w, pad_h,
                                sfx_hit, y_speeds, play_snd):
        """
        If ball touches either paddle, return a new (vx, vy) tuple;
        otherwise return None.
        """
        x_ball, y_ball = ball.get_pos()
        ball_bot = y_ball + ball.get_height()

        for paddle, is_right in ((right_pad, True), (left_pad, False)):
            if CollisionManager._overlaps_paddle(
                x_ball, y_ball, ball_bot,
                *paddle.get_pos(), pad_w, pad_h, is_right
            ):
                play_snd(sfx_hit)
                direction = -1 if is_right else +1
                new_vx = direction * (abs(vx) + BallSpeedPix)
                new_vy = random.choice(y_speeds)
                return new_vx, new_vy
        return None

    @staticmethod
    def handle_wall_collision(y_ball, vy, ball_h):
        """Bounce off top / bottom walls — return new vy or None."""
        if y_ball <= 0:
            return  abs(vy)
        if y_ball >= gHeight - ball_h:
            return -abs(vy)
        return None

    @staticmethod
    def handle_side_collision(ball, idx, x_ball, sfx):
        """
        Ball exited field → play SFX, respawn, update lives,
        maybe trigger game-over. Returns new (vx, vy).
        """
        CollisionManager._play_sound(sfx[1])

        new_vx = random.choice((-BallSpeedPix, BallSpeedPix))
        new_vy = random.choice((-BallSpeedPix, BallSpeedPix))
        ball.update_Move(new_vx, new_vy)

        CollisionManager._center_ball(idx)
        CollisionManager._update_lives_after_score(x_ball)
        CollisionManager.check_game_over()

        return new_vx, new_vy

    @staticmethod
    def check_game_over():
        """Display winner screen when either side reaches 0 lives."""
        pads = list(GlobalData.sprite_list)
        if len(pads) != 2:
            return

        left_life, right_life = pads[0].get_life()[0], pads[1].get_life()[1]

        if left_life <= 0:
            winner = "Computer" if GlobalData.against_com else "Right"
            GameTextManager.game_over_message(winner)
            CollisionManager._wait_for_restart()
        elif right_life <= 0:
            GameTextManager.game_over_message("Left")
            CollisionManager._wait_for_restart()

    # =========================================================
    #  PRIVATE HELPERS
    # =========================================================
    @staticmethod
    def _wait_for_restart():
        """Block until user presses a key — restart or quit."""
        clock = pygame.time.Clock()
        from pongGame import start_game          # late import avoids cycle
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    start_game()
            clock.tick(REFRESH)

    @staticmethod
    def _center_ball(idx):
        """Reset the idx-th ball to screen centre."""
        balls = list(GlobalData.ball_list)
        if idx >= len(balls):
            return
        ball = balls[idx]
        cx = gWidth  / 2 - ball.get_width()  / 2
        cy = gHeight / 2 - ball.get_height() / 2
        ball.update_loc(cx, cy)

    @staticmethod
    def _update_lives_after_score(x_ball):
        """Decrease the proper paddle’s life counter."""
        pads = list(GlobalData.sprite_list)
        if len(pads) != 2:
            return
        if x_ball <= 0:
            pads[0].lose_life("left")
        else:
            pads[1].lose_life("right")

    @staticmethod
    def _overlaps_paddle(x_ball, y_ball, y_bot,
                         x_pad, y_pad, pad_w, pad_h, is_right):
        """Return True when ball overlaps paddle area."""
        vertical = y_bot >= y_pad and y_ball <= y_pad + pad_h
        if not vertical:
            return False
        return (x_ball >= x_pad - Xdeviation - pad_w) if is_right \
               else (x_ball <= x_pad + Xdeviation)

    @staticmethod
    def _play_sound(sound):
        """Non-blocking SFX helper."""
        channel = pygame.mixer.find_channel()
        if channel:
            channel.queue(sound)

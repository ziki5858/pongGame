import pygame
from constantsGlobal import (
    gWidth, WHITE, RED, BallSpeedPix, GlobalData
)
from GameBoardManager import GameBoardManager
from CollisionManager import CollisionManager


class BallManager:
    """Static manager: updates ball logic, plays SFX and redraws board."""

    # ------------------------------------------------------------------
    # Static “assets” – loaded once
    # ------------------------------------------------------------------
    _SOUNDS: list[pygame.mixer.Sound] = []
    _Y_SPEEDS: tuple[int, int] = (+BallSpeedPix, -BallSpeedPix)

    # ------------------------  public API  -----------------------------

    @staticmethod
    def init_sounds():
        """Load sound effects (call once at program start)."""
        if BallManager._SOUNDS:        # already loaded
            return
        pygame.mixer.init(frequency=22_050, size=-16, channels=4)
        BallManager._SOUNDS = [
            pygame.mixer.Sound("Swipe Swoosh Transition Sound Effect.mp3"),
            pygame.mixer.Sound("Video Game Beep - Sound Effect.mp3"),
        ]

    @staticmethod
    def move_balls():
        """Move every ball, handle collisions, then redraw the screen."""
        paddles = list(GlobalData.sprite_list)
        if len(paddles) != 2:
            return                     # safety: need exactly 2 paddles
        left_pad, right_pad = paddles

        for idx, ball in enumerate(GlobalData.ball_list):
            BallManager._move_single_ball(
                ball, idx, left_pad, right_pad
            )

        BallManager._redraw_screen()

    # *legacy name*  – used by older code such as pongGame.py
    ball_move = move_balls

    # ------------------------  internals  ------------------------------

    @staticmethod
    def _move_single_ball(ball, idx, left_pad, right_pad):
        """Physics + scoring for one ball in the list."""
        x, y = ball.get_pos()
        vx, vy = ball.get_move()

        # 1. Paddle collision
        new_vel = CollisionManager.handle_paddle_collision(
            ball, left_pad, right_pad,
            vx,
            right_pad.get_width(), right_pad.get_height(),
            BallManager._SOUNDS[0],
            BallManager._Y_SPEEDS,
            BallManager.play_sound,
        )
        if new_vel:
            vx, vy = new_vel

        # 2. Wall collision (top/bottom)
        else:
            wall_vy = CollisionManager.handle_wall_collision(
                y, vy, ball.get_height()
            )
            if wall_vy is not None:
                vy = wall_vy

            # 3. Side collision (score / out-of-bounds)
            elif x <= 0 or x >= gWidth - ball.get_width():
                vx, vy = CollisionManager.handle_side_collision(
                    ball, idx, x, BallManager._SOUNDS
                )

        BallManager._apply_motion(ball, vx, vy)
        CollisionManager.check_game_over()

    # --- tiny helpers --------------------------------------------------

    @staticmethod
    def _apply_motion(ball, vx, vy):
        """Write new velocity and advance the ball by one step."""
        ball.update_Move(vx, vy)            # keep legacy name!
        x, y = ball.get_pos()
        ball.update_loc(x + vx, y + vy)

    @staticmethod
    def _redraw_screen():
        """Clear, draw board & flip once per frame."""
        GameBoardManager.r_screen(WHITE, RED)
        pygame.display.flip()

    # ------------------------  SFX helper ------------------------------

    @staticmethod
    def play_sound(sound: pygame.mixer.Sound):
        """Play given SFX on the first free channel (non-blocking)."""
        channel = pygame.mixer.find_channel()
        if channel:
            channel.queue(sound)

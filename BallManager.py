import sys
from constantsGlobal import *
from GameBoardManager import GameBoardManager
from GameTextManager import GameTextManager
from CollisionManager import CollisionManager

class BallManager:
    """Static manager for ball movement, collisions, and sound effects."""
    sounds = []

    @staticmethod
    def init_sounds():
        """Initialize mixer and load sound effects."""
        pygame.mixer.init(frequency=22050, size=-16, channels=4)
        BallManager.sounds = [
            pygame.mixer.Sound('Swipe Swoosh Transition Sound Effect.mp3'),
            pygame.mixer.Sound('Video Game Beep - Sound Effect.mp3'),
        ]

    @staticmethod
    def move_balls():
        """Move all balls: handle collisions and redraw the game board."""
        y_speeds = [abs(BallSpeedPix), -abs(BallSpeedPix)]
        paddles = list(GlobalData.sprite_list)
        if len(paddles) != 2:
            return
        left_paddle, right_paddle = paddles

        for idx, ball in enumerate(GlobalData.ball_list):
            BallManager._move_single_ball(
                ball, idx,
                left_paddle, right_paddle,
                right_paddle.get_width(), right_paddle.get_height(),
                y_speeds
            )

        # Redraw background and flip display
        GameBoardManager.r_screen(WHITE, RED)
        pygame.display.flip()

    ball_move = move_balls  # Legacy alias

    @staticmethod
    def _move_single_ball(ball, idx, left_paddle, right_paddle,
                          paddle_w, paddle_h, y_speeds):
        """Handle movement, collision, and sound for a single ball."""
        x_pos, y_pos = ball.get_pos()
        x_move, y_move = ball.get_move()

        # Paddle collision
        result = CollisionManager.handle_paddle_collision(
            ball, left_paddle, right_paddle,
            x_move, paddle_w, paddle_h,
            BallManager.sounds[0], y_speeds,
            BallManager.play_sound
        )
        if result:
            x_move, y_move = result
        else:
            # Wall collision
            wall_res = CollisionManager.handle_wall_collision(
                y_pos, y_move, ball.get_height()
            )
            if wall_res is not None:
                y_move = wall_res
            else:
                # Side collision and scoring
                if x_pos <= 0 or x_pos >= gWidth - ball.get_width():
                    x_move, y_move = CollisionManager.handle_side_collision(
                        ball, idx, x_pos, BallManager.sounds
                    )

        BallManager._update_and_draw(ball, x_move, y_move)
        BallManager._check_game_over(
            left_paddle.get_life(), right_paddle.get_life()
        )

    @staticmethod
    def _update_and_draw(ball, x_move, y_move):
        """Update ball position and draw on screen."""
        ball.update_Move(x_move, y_move)
        x, y = ball.get_pos()
        ball.update_loc(x + x_move, y + y_move)

    @staticmethod
    def _check_game_over(left_life, right_life):
        """Trigger game over sequence if a paddle's life reaches zero."""
        if left_life == 0:
            GameTextManager.game_over_message(
                'Computer' if GlobalData.against_com else 'Right'
            )
            BallManager._wait_for_restart()
        elif right_life == 0:
            GameTextManager.game_over_message('Left')
            BallManager._wait_for_restart()

    @staticmethod
    def _wait_for_restart():
        """Pause game until the user presses a key to restart or quit."""
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    from pongGame import start_game
                    start_game()
            clock.tick(REFRESH)

    @staticmethod
    def play_sound(sound):
        """Queue a sound effect on the next available mixer channel."""
        channel = pygame.mixer.find_channel()
        if channel:
            channel.queue(sound)

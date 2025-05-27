"""
BallManager.py

Manages ball behavior, collisions, sounds, and game-over state.
Contains:
- init_sounds(): load sound effects.
- move_balls(): iterate through balls, handle collisions, update positions.
- ball_move: alias for move_balls (backward compatibility).
- _move_single_ball(): collision logic for paddle, walls, sides.
- _update_and_draw(): update ball position and draw.
- _check_game_over(): triggers game-over sequence.
- _wait_for_restart(): waits for user to restart or quit.
- play_sound(): queues sound effect on mixer.

Dependencies: pygame, GlobalData, GameTextManager, GameBoardManager,
CollisionManager, constants
"""

import sys
import random
import pygame
import GlobalData
from GameBoardManager import GameBoardManager
from GameTextManager import GameTextManager
from CollisionManager import CollisionManager
from constants import gWidth, WHITE, RED, REFRESH, BallSpeedPix


class BallManager:
    """Static manager for ball movement, collisions, and sound effects."""

    sounds = []

    @staticmethod
    def init_sounds():
        """
        Initialize mixer and load sound effects into BallManager.sounds.
        """
        pygame.mixer.init(frequency=22050, size=-16, channels=4)
        BallManager.sounds = [
            pygame.mixer.Sound('Swipe Swoosh Transition Sound Effect.mp3'),
            pygame.mixer.Sound('Video Game Beep - Sound Effect.mp3')
        ]

    @staticmethod
    def move_balls():
        """
        Move all balls: handle collisions and redraw board.
        """
        y_speeds = [abs(BallSpeedPix), -abs(BallSpeedPix)]
        paddles = GlobalData.sprite_list.sprites()
        if len(paddles) != 2:
            return
        left_paddle, right_paddle = paddles

        for idx, ball in enumerate(GlobalData.ball_list.sprites()):
            BallManager._move_single_ball(
                ball, idx, left_paddle, right_paddle,
                right_paddle.get_width(), right_paddle.get_height(),
                y_speeds
            )

        GameBoardManager.r_screen(WHITE, RED)
        pygame.display.flip()

    # Alias for legacy code
    ball_move = move_balls

    @staticmethod
    def _move_single_ball(ball, idx, left_paddle, right_paddle,
                          paddle_w, paddle_h, y_speeds):
        """
        Handle movement and collision for a single ball.
        """
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
            # Wall collision (top/bottom)
            wall_res = CollisionManager.handle_wall_collision(
                y_pos, y_move, ball.get_height()
            )
            if wall_res is not None:
                y_move = wall_res
            else:
                # Side collision (scores)
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
        """
        Update ball's position data and draw it at new location.
        """
        ball.update_Move(x_move, y_move)
        x, y = ball.get_pos()
        ball.update_loc(x + x_move, y + y_move)

    @staticmethod
    def _check_game_over(left_life, right_life):
        """
        If a paddle's life reaches zero, display game over and wait.
        """
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
        """
        Pause game loop; wait for key press to restart or quit.
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
    def play_sound(sound):
        """
        Queue a sound effect on the next available mixer channel.
        """
        channel = pygame.mixer.find_channel()
        if channel:
            channel.queue(sound)

import random
import pygame
from constants import *
import GlobalData
from GameBoardManager import GameBoardManager
from GameTextManager import GameTextManager
from CollisionManager import CollisionManager

class BallManager:
    soundList = []

    @staticmethod
    def init_sounds():
        pygame.mixer.init(frequency=22050, size=-16, channels=4)
        BallManager.soundList = [
            pygame.mixer.Sound('Swipe Swoosh Transition Sound Effect.mp3'),
            pygame.mixer.Sound('Video Game Beep - Sound Effect.mp3')
        ]

    @staticmethod
    def ball_move():
        y_speeds = [abs(BallSpeedPix), -abs(BallSpeedPix)]
        left_paddle, right_paddle = GlobalData.sprite_list.sprites()
        paddle_w = right_paddle.get_width()
        paddle_h = right_paddle.get_height()

        for i, ball in enumerate(GlobalData.ball_list.sprites()):
            BallManager.move_single_ball(ball, i, left_paddle, right_paddle, paddle_w, paddle_h, y_speeds)

        GameBoardManager.r_screen(WHITE, RED)

    @staticmethod
    def move_single_ball(ball, i, left_paddle, right_paddle, paddle_w, paddle_h, y_speeds):
        xBall, yBall = ball.get_pos()
        xMove, yMove = ball.get_move()

        paddle_result = CollisionManager.handle_paddle_collision(
            ball, left_paddle, right_paddle, xMove,
            paddle_w, paddle_h, BallManager.soundList[0], y_speeds, BallManager.sound
        )
        if paddle_result:
            xMove, yMove = paddle_result
        else:
            wall_result = CollisionManager.handle_wall_collision(yBall, yMove, ball.get_height())
            if wall_result is not None:
                yMove = wall_result
            else:
                if xBall <= 0 or xBall >= gWidth - ball.get_width():
                    xMove, yMove = CollisionManager.handle_side_collision(ball, i, xBall, BallManager.soundList)

        BallManager.update_and_draw(ball, xMove, yMove)

        # check game over after lives were updated
        left_life = left_paddle.get_life()
        right_life = right_paddle.get_life()
        BallManager.check_game_over(left_life, right_life)

    @staticmethod
    def update_and_draw(ball, xMove, yMove):
        ball.update_Move(xMove, yMove)
        x, y = ball.get_pos()
        ball.update_loc(x + xMove, y + yMove)

    @staticmethod
    def check_game_over(leftLife, rightLife):
        if leftLife == 0:
            GameTextManager.game_over_message('Right' if not GlobalData.against_com else 'computer')
            BallManager.wait_after_game_over(restart=True)
        elif rightLife == 0:
            GameTextManager.game_over_message("Left")
            BallManager.wait_after_game_over(restart=True)

    @staticmethod
    def wait_after_game_over(restart=False):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if restart:
                        from pongGame import start_game
                        start_game()
                    else:
                        pygame.quit()
                        exit()
            clock.tick(REFRESH)

    @staticmethod
    def sound(soundNumber):
        channel = pygame.mixer.find_channel()
        if channel is not None:
            channel.queue(soundNumber)

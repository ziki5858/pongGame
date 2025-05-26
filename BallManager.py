import random
import pygame
from constants import *
import GlobalData
from GameBoardManager import GameBoardManager
from GameTextManager import GameTextManager

class BallManager:
    @staticmethod
    def ball_move():
        rList = [abs(BallSpeedPix), -abs(BallSpeedPix)]
        soundList = BallManager.upload_sound()
        left_paddle, right_paddle = GlobalData.sprite_list.sprites()
        paddle_w = right_paddle.get_width()
        paddle_h = right_paddle.get_height()

        for i, ball in enumerate(GlobalData.ball_list.sprites()):
            BallManager.check_game_over(*left_paddle.get_life())
            xBall, yBall = ball.get_pos()
            xMove, yMove = ball.get_move()

            paddle_result = BallManager.handle_paddle_collision(
                ball, left_paddle, right_paddle, xMove,
                paddle_w, paddle_h, soundList[0], rList
            )
            if paddle_result:
                xMove, yMove = paddle_result
            else:
                wall_result = BallManager.handle_wall_collision(yBall, yMove, ball.get_height())
                if wall_result is not None:
                    yMove = wall_result
                else:
                    if xBall <= 0 or xBall >= gWidth - ball.get_width():
                        xMove, yMove = BallManager.handle_side_collision(ball, soundList, i)

            BallManager.update_and_draw(ball, xMove, yMove)

        GameBoardManager.r_screen(WHITE, RED)

    @staticmethod
    def update_and_draw(ball, xMove, yMove):
        ball.update_Move(xMove, yMove)
        x, y = ball.get_pos()
        ball.update_loc(x + xMove, y + yMove)

    @staticmethod
    def handle_paddle_collision(ball, left_paddle, right_paddle, xMove, paddle_w, paddle_h, sound_effect, rList):
        xBall, yBall = ball.get_pos()
        for paddle, side in ((right_paddle, 'r'), (left_paddle, 'l')):
            if BallManager.check_borders_ball(
                xBall, yBall, *paddle.get_pos(), paddle_w,
                paddle_h, side, yBall + ball.get_height()
            ):
                BallManager.sound(sound_effect)
                direction = -1 if side == 'r' else 1
                new_x = direction * abs(xMove) + direction * AddSpeedBall
                new_y = random.choice(rList)
                return new_x, new_y
        return None

    @staticmethod
    def handle_wall_collision(yBall, yMove, ball_height):
        if yBall <= 0:
            return abs(yMove)
        if yBall >= gHeight - ball_height:
            return -abs(yMove)
        return None

    @staticmethod
    def handle_side_collision(ball, soundList, index):
        BallManager.edgePoint(soundList, index)
        xBall, _ = ball.get_pos()
        if xBall <= 0:
            return BallSpeedPix, -BallSpeedPix
        return -BallSpeedPix, BallSpeedPix

    @staticmethod
    def edgePoint(soundList, i):
        BallManager.sound(soundList[1])
        BallManager.ball_to_center(i)
        GlobalData.sprite_list.sprites()[0].update_right_Life()

    @staticmethod
    def ball_to_center(i):
        GlobalData.ball_list.sprites()[i].update_loc(
            (gWidth / 2 - GlobalData.ball_list.sprites()[0].get_width() / 2),
            (gHeight / 2 - GlobalData.ball_list.sprites()[0].get_height() / 2)
        )

    @staticmethod
    def check_borders_ball(x_ball, y_ball, x_paddle, y_paddle, paddle_width, paddle_height, paddle_side, y_ball_bottom):
        if y_ball_bottom < y_paddle or y_ball > y_paddle + paddle_height:
            return False
        if paddle_side == 'r':
            return x_ball >= x_paddle - Xdeviation - paddle_width
        else:
            return x_ball <= x_paddle + Xdeviation

    @staticmethod
    def check_game_over(leftLife, rightLife):
        if leftLife == 0:
            GameTextManager.game_over_message('Right' if not GlobalData.against_com else 'computer')
        elif rightLife == 0:
            GameTextManager.game_over_message("Left")

    @staticmethod
    def sound(soundNumber):
        channel = pygame.mixer.find_channel()
        if channel is not None:
            channel.queue(soundNumber)

    @staticmethod
    def upload_sound():
        pygame.mixer.init(frequency=22050, size=-16, channels=4)
        return [
            pygame.mixer.Sound('Swipe Swoosh Transition Sound Effect.mp3'),
            pygame.mixer.Sound('Video Game Beep - Sound Effect.mp3')
        ]

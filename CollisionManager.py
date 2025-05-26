import random
import pygame
from constants import *
import GlobalData

class CollisionManager:
    @staticmethod
    def handle_paddle_collision(ball, left_paddle, right_paddle, xMove, sound_effect, y_speeds, sound_func):
        xBall, yBall = ball.get_pos()
        for paddle, side in ((right_paddle, 'r'), (left_paddle, 'l')):
            paddle_x, paddle_y = paddle.get_pos()
            if CollisionManager.check_borders_ball(
                xBall, yBall, paddle_x, paddle_y,
                paddle.get_width(), paddle.get_height(), side,
                yBall + ball.get_height()
            ):
                sound_func(sound_effect)
                direction = -1 if side == 'r' else 1
                new_x = direction * abs(xMove) + direction * AddSpeedBall
                new_y = random.choice(y_speeds)
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
    def handle_side_collision(ball, index, xBall, soundList):
        CollisionManager.sound(soundList[1])
        CollisionManager.ball_to_center(index)

        if xBall <= 0:
            GlobalData.sprite_list.sprites()[0].lose_life()
            return BallSpeedPix, -BallSpeedPix
        else:
            GlobalData.sprite_list.sprites()[1].lose_life()
            return -BallSpeedPix, BallSpeedPix

    @staticmethod
    def ball_to_center(i):
        ball = GlobalData.ball_list.sprites()[i]
        ball.rect.center = (gWidth // 2, gHeight // 2)

    @staticmethod
    def check_borders_ball(x_ball, y_ball, x_paddle, y_paddle, paddle_width, paddle_height, paddle_side, y_ball_bottom):
        if y_ball_bottom < y_paddle or y_ball > y_paddle + paddle_height:
            return False
        return x_ball >= x_paddle - Xdeviation - paddle_width if paddle_side == 'r' else x_ball <= x_paddle + Xdeviation

    @staticmethod
    def sound(soundNumber):
        channel = pygame.mixer.find_channel()
        if channel is not None:
            channel.queue(soundNumber)

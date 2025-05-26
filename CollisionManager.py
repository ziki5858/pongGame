import pygame
import random
import GlobalData
from constants import *
from GameTextManager import GameTextManager

class CollisionManager:
    @staticmethod
    def handle_paddle_collision(ball, left_paddle, right_paddle, xMove, paddle_w, paddle_h, sound_effect, y_speeds, sound_func):
        xBall, yBall = ball.get_pos()
        for paddle, side in ((right_paddle, 'r'), (left_paddle, 'l')):
            if CollisionManager.check_borders_ball(
                xBall, yBall, *paddle.get_pos(), paddle_w,
                paddle_h, side, yBall + ball.get_height()
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

        # Spread balls to random direction when respawning
        new_x = random.choice([-BallSpeedPix, BallSpeedPix])
        new_y = random.choice([-BallSpeedPix, BallSpeedPix])

        ball.update_Move(new_x, new_y)
        CollisionManager.ball_to_center(index)

        if xBall <= 0:
            GlobalData.sprite_list.sprites()[0].lose_life('left')
        else:
            GlobalData.sprite_list.sprites()[1].lose_life('right')

        CollisionManager.check_game_over()
        return new_x, new_y

    @staticmethod
    def check_game_over():
        left = GlobalData.sprite_list.sprites()[0].get_life()[0]
        right = GlobalData.sprite_list.sprites()[1].get_life()[1]
        if left <= 0:
            GameTextManager.game_over_message('Right' if not GlobalData.against_com else 'computer')
            CollisionManager.wait_after_game_over()
        elif right <= 0:
            GameTextManager.game_over_message('Left')
            CollisionManager.wait_after_game_over()

    @staticmethod
    def wait_after_game_over():
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    from pongGame import start_game
                    start_game()
            clock.tick(REFRESH)

    @staticmethod
    def ball_to_center(i):
        ball = GlobalData.ball_list.sprites()[i]
        center_x = gWidth / 2 - ball.get_width() / 2
        center_y = gHeight / 2 - ball.get_height() / 2
        ball.update_loc(center_x, center_y)

    @staticmethod
    def check_borders_ball(x_ball, y_ball, x_paddle, y_paddle, paddle_width, paddle_height, paddle_side, y_ball_bottom):
        if y_ball_bottom < y_paddle or y_ball > y_paddle + paddle_height:
            return False
        if paddle_side == 'r':
            return x_ball >= x_paddle - Xdeviation - paddle_width
        else:
            return x_ball <= x_paddle + Xdeviation

    @staticmethod
    def sound(soundNumber):
        channel = pygame.mixer.find_channel()
        if channel is not None:
            channel.queue(soundNumber)

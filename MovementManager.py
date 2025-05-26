import pygame
from constants import *
import GlobalData

class MovementManager:
    UP_DOWN_LEFT = [pygame.K_s, pygame.K_w]
    UP_DOWN_RIGHT = [pygame.K_DOWN, pygame.K_UP]
    sprite_speed = 25

    @staticmethod
    def get_paddles():
        sprites = GlobalData.sprite_list.sprites()
        return sprites[0], sprites[1]

    @staticmethod
    def get_positions(lSprite, rSprite):
        xL, yL = lSprite.get_pos()
        xR, yR = rSprite.get_pos()
        xB, yB = GlobalData.ball_list.sprites()[0].get_pos()
        return xL, yL, xR, yR, xB, yB

    @staticmethod
    def handle_player_move(event, sprite, x, y, key_map, speed):
        for dir_idx, key in enumerate(key_map):
            if event.key == key:
                new_y = MovementManager.checkBorderS(y, speed[dir_idx], sprite.get_height())
                sprite.update_loc(x, new_y)
                break

    @staticmethod
    def handle_ai_move(rSprite, xR, yR, ball_center, max_step):
        paddle_center = yR + rSprite.get_height() * 0.5
        delta = ball_center - paddle_center
        dead_zone = 10
        if abs(delta) <= dead_zone:
            step = 0
        else:
            step = max(-max_step, min(delta, max_step))
        new_y = MovementManager.checkBorderS(yR, step, rSprite.get_height())
        rSprite.update_loc(xR, new_y)

    @staticmethod
    def sprite_movement(event):
        lSprite, rSprite = MovementManager.get_paddles()
        xL, yL, xR, yR, xB, yB = MovementManager.get_positions(lSprite, rSprite)
        speed = MovementManager.sprite_speed
        ball = GlobalData.ball_list.sprites()[0]
        ball_center = yB + ball.get_height() * 0.5

        if event is not None:
            MovementManager.handle_player_move(event, lSprite, xL, yL, MovementManager.UP_DOWN_LEFT, [speed, -speed])
            if not GlobalData.against_com:
                MovementManager.handle_player_move(event, rSprite, xR, yR, MovementManager.UP_DOWN_RIGHT, [speed, -speed])

        if GlobalData.against_com:
            MovementManager.handle_ai_move(rSprite, xR, yR, ball_center, speed)

    @staticmethod
    def checkBorderS(object_y, move_amount, paddle_height):
        if 0 > object_y + move_amount:
            return 0
        elif object_y + move_amount > gHeight - paddle_height:
            return gHeight - paddle_height
        return object_y + move_amount
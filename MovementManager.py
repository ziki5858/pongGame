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
    def get_paddle_and_ball_positions(lSprite, rSprite):
        xL, yL = lSprite.get_pos()
        xR, yR = rSprite.get_pos()
        xB, yB = GlobalData.ball_list.sprites()[0].get_pos()
        return xL, yL, xR, yR, xB, yB

    @staticmethod
    def handle_player_move(event, sprite, x, y, key_map, speed):
        for dir_idx, key in enumerate(key_map):
            if event.key == key:
                new_y = MovementManager.constrain_paddle_position(y, speed[dir_idx], sprite.get_height())
                sprite.update_loc(x, new_y)
                break

    @staticmethod
    def _move_player_if_key(event, sprite, x, y, key_map):
        speeds = [MovementManager.sprite_speed, -MovementManager.sprite_speed]
        MovementManager.handle_player_move(event, sprite, x, y, key_map, speeds)

    @staticmethod
    def handle_ai_move(rSprite, xR, yR, ball_center, max_step):
        paddle_center = yR + rSprite.get_height() * 0.5
        delta = ball_center - paddle_center
        dead_zone = 10
        if abs(delta) <= dead_zone:
            step = 0
        else:
            step = max(-max_step, min(delta, max_step))
        new_y = MovementManager.constrain_paddle_position(yR, step, rSprite.get_height())
        rSprite.update_loc(xR, new_y)

    @staticmethod
    def sprite_movement(event):
        lSprite, rSprite = MovementManager.get_paddles()
        xL, yL, xR, yR, xB, yB = MovementManager.get_paddle_and_ball_positions(lSprite, rSprite)
        ball = GlobalData.ball_list.sprites()[0]
        ball_center = yB + ball.get_height() * 0.5

        if event:
            MovementManager._move_player_if_key(event, lSprite, xL, yL, MovementManager.UP_DOWN_LEFT)
            if not GlobalData.against_com:
                MovementManager._move_player_if_key(event, rSprite, xR, yR, MovementManager.UP_DOWN_RIGHT)

        if GlobalData.against_com:
            MovementManager.handle_ai_move(rSprite, xR, yR, ball_center, MovementManager.sprite_speed)

    @staticmethod
    def constrain_paddle_position(current_y, move_amount, paddle_height):
        new_y = current_y + move_amount
        if new_y < 0:
            return 0
        elif new_y > gHeight - paddle_height:
            return gHeight - paddle_height
        return new_y
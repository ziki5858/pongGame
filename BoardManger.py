import pygame
from constants import *
import GlobalData
from player import Player
from ball import Ball

def upload_screen(title, bColor, sColor):
    pygame.init()
    GlobalData.screen = pygame.display.set_mode((gWidth, gHeight))
    GlobalData.screen.fill(bColor)
    pygame.display.set_caption(str(title))
    from pongGame import againstWho  # ייבוא מאוחר כדי למנוע לולאת ייבוא
    GlobalData.against_com = againstWho()
    GlobalData.screen.fill(bColor)
    pygame.draw.line(GlobalData.screen, sColor, (gWidth / 2, 0), (gWidth / 2, gHeight), 2)
    pygame.display.flip()

def upload_sprites():
    GlobalData.sprite_list.empty()
    GlobalData.ball_list.empty()

    left_paddle = Player(0, gHeight / 2)
    paddle_width = left_paddle.get_width()
    right_paddle = Player(gWidth - paddle_width, gHeight / 2)
    GlobalData.sprite_list.add(left_paddle, right_paddle)

    for _ in range(BALL_AMOUNT):
        GlobalData.ball_list.add(Ball(gWidth / 2, gHeight / 2))

    GlobalData.sprite_list.draw(GlobalData.screen)
    GlobalData.ball_list.draw(GlobalData.screen)
    pygame.display.flip()

import pygame
from constants import *
import GlobalData
from player import Player
from ball import Ball
from GameTextManager import GameTextManager

class GameBoardManager:
    @staticmethod
    def upload_screen(title, bColor, sColor):
        pygame.init()
        GlobalData.screen = pygame.display.set_mode((gWidth, gHeight))
        pygame.display.set_caption(str(title))

        from pongGame import againstWho  # delayed import to avoid circular dependency
        GlobalData.against_com = againstWho()

        GameBoardManager.clear_screen(bColor)
        GameBoardManager.draw_center_line(sColor)

    @staticmethod
    def upload_sprites():
        GlobalData.sprite_list.empty()
        GlobalData.ball_list.empty()

        left_paddle = Player(0, gHeight / 2, GlobalData.player_life)
        right_paddle = Player(gWidth - left_paddle.get_width(), gHeight / 2, GlobalData.player_life)
        GlobalData.sprite_list.add(left_paddle, right_paddle)

        for _ in range(GlobalData.ball_amount):
            GlobalData.ball_list.add(Ball(gWidth / 2, gHeight / 2))

        GameBoardManager.redraw()

    @staticmethod
    def r_screen(bColor, sColor):
        GameBoardManager.clear_screen(bColor)
        GameBoardManager.draw_center_line(sColor)
        GameBoardManager.redraw()
        GameTextManager.show_score()
        pygame.display.flip()

    @staticmethod
    def clear_screen(color):
        GlobalData.screen.fill(color)

    @staticmethod
    def draw_center_line(color):
        pygame.draw.line(GlobalData.screen, color, (gWidth // 2, 0), (gWidth // 2, gHeight), 2)

    @staticmethod
    def redraw():
        GlobalData.sprite_list.draw(GlobalData.screen)
        GlobalData.ball_list.draw(GlobalData.screen)

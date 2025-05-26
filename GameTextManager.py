import pygame
import constants
import GlobalData
from constants import BLACK, WHITE, RED, gWidth, gHeight, BALL_AMOUNT
class GameTextManager:
    @staticmethod
    def captions(font_size, caption, size, color, x, y, flip):
        font = pygame.font.Font(None, font_size)
        text1 = font.render(caption, size, color)
        GlobalData.screen.blit(text1, (x, y))
        if flip:
            pygame.display.flip()

    @staticmethod
    def show_score():
        left = GlobalData.sprite_list.sprites()[0].get_life()
        right = GlobalData.sprite_list.sprites()[1].get_life()

        font = pygame.font.Font(None, 50)
        text1 = font.render(f'Left: {left}', True, BLACK)
        GlobalData.screen.blit(text1, (20, 30))

        text2 = font.render(f'Right: {right}', True, BLACK)
        GlobalData.screen.blit(text2, (310, 30))

    @staticmethod
    def game_over_message(winner):
        GlobalData.screen.fill(WHITE)
        GameTextManager.captions(40, 'Game over:  ' + winner + '  win', 1, BLACK, 65, 200, False)
        GameTextManager.captions(25, 'Press keyBord to reGame', 1, RED, 160, 250, True)

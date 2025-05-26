import pygame
from constants import *
import GlobalData

class GameTextManager:
    @staticmethod
    def draw_text(text, font_size, antialias, color, x, y, flip=False):
        font = pygame.font.Font(None, font_size)
        rendered = font.render(text, antialias, color)
        GlobalData.screen.blit(rendered, (x, y))
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
        GameTextManager.draw_text(f'Game over: {winner} wins', 40, True, BLACK, 65, 200)
        GameTextManager.draw_text('Press any key to play again', 25, True, RED, 120, 250, flip=True)

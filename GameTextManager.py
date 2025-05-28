import pygame
from constants import *
import GlobalData

class GameTextManager:
    """Handles all game text and center line rendering."""

    @staticmethod
    def draw_text(text, font_size, antialias, color, x, y, flip=False):
        """Draw text at given position; flip display if requested."""
        font = pygame.font.Font(None, font_size)
        rendered = font.render(text, antialias, color)
        GlobalData.screen.blit(rendered, (x, y))
        if flip:
            pygame.display.flip()

    @staticmethod
    def show_score():
        """Render the current left and right scores."""
        left = GlobalData.sprite_list.sprites()[0].get_life()[0]
        right = GlobalData.sprite_list.sprites()[1].get_life()[1]

        font = pygame.font.Font(None, 50)
        text1 = font.render(f'Left: {left}', True, BLACK)
        GlobalData.screen.blit(text1, (20, 30))

        text2 = font.render(f'Right: {right}', True, BLACK)
        GlobalData.screen.blit(text2, (310, 30))

    @staticmethod
    def draw_center_line():
        """Draw improved dashed center line."""
        width, height = GlobalData.screen.get_size()
        dash, gap = 15, 10
        y = 0
        while y < height:
            pygame.draw.line(
                GlobalData.screen,
                WHITE,
                (width // 2, y),
                (width // 2, y + dash),
                4
            )
            y += dash + gap

    @staticmethod
    def game_over_message(winner):
        """Fill screen and display game over text and restart prompt."""
        GlobalData.screen.fill(WHITE)
        GameTextManager.draw_center_line()
        GameTextManager.draw_text(f'Game over: {winner} wins', 40, True, BLACK, 65, 200)
        GameTextManager.draw_text('Press any key to play again', 25, True, RED, 120, 250, flip=True)
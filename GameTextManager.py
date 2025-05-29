from constantsGlobal import *
import math

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
    def draw_gradient_background(screen, width, height, top_color_base, bottom_color_base):
        """
        Draws a pulsating vertical gradient background on the entire screen.
        """
        t = pygame.time.get_ticks()
        pulse = (math.sin(t * 0.005) + 1) / 2

        # interpolate between top and bottom base colors
        top_color = [
            int(top_color_base[i] * (1 - pulse) + bottom_color_base[i] * pulse)
            for i in range(3)
        ]
        bottom_color = [
            int(bottom_color_base[i] * (1 - pulse) + top_color_base[i] * pulse)
            for i in range(3)
        ]

        # draw gradient one horizontal line at a time
        for y in range(height):
            ratio = y / (height - 1)
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    @staticmethod
    def draw_menu(screen, width, height, prompt, options, title_font, option_font):
        """
        Renders a centered title and a list of selectable options.
        Each option is drawn with a semi-transparent backdrop for readability.
        """
        # render title shadow and main title
        shadow = title_font.render(prompt, True, BLACK)
        title_surf = title_font.render(prompt, True, RED)
        title_w, title_h = title_surf.get_size()

        # blit shadow slightly offset
        screen.blit(shadow, ((width - title_w) // 2 + 3, height // 4 + 3))
        # blit main title
        screen.blit(title_surf, ((width - title_w) // 2, height // 4))

        # render each option
        for text, color, pos_y in options:
            surf = option_font.render(text, True, color)
            rect = surf.get_rect(center=(width // 2, pos_y))

            # translucent background panel
            bg = pygame.Surface((rect.width + 20, rect.height + 10), pygame.SRCALPHA)
            bg.fill((255, 255, 255, 100))
            screen.blit(bg, bg.get_rect(center=rect.center))
            screen.blit(surf, rect)

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
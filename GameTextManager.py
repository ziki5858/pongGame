import math
from constantsGlobal import *


class GameTextManager:
    """Handles all game text, centre line, menus and settings UI."""
    _FONTS = {}       # Cache for Font objects to avoid reloading

    @staticmethod
    def _get_font(size):
        """Return a cached Font object for the requested size."""
        if size not in GameTextManager._FONTS:
            GameTextManager._FONTS[size] = pygame.font.Font(None, size)
        return GameTextManager._FONTS[size]

    # ------------------------------------------------------------------
    # Basic text helpers
    # ------------------------------------------------------------------
    @staticmethod
    def draw_text(text, font_size, antialias, color, x, y, flip=False):
        """Draw text at given position; flip display if requested."""
        font = GameTextManager._get_font(font_size)
        rendered = font.render(text, antialias, color)
        GlobalData.screen.blit(rendered, (x, y))
        if flip:
            pygame.display.flip()

    @staticmethod
    def font_width(text, font_size):
        """Return width in pixels of rendered text (for centring)."""
        font = GameTextManager._get_font(font_size)
        return font.size(text)[0]

    # ------------------------------------------------------------------
    # Backgrounds & menus
    # ------------------------------------------------------------------
    @staticmethod
    def draw_gradient_background(screen, width, height,
                                 top_color_base, bottom_color_base):
        """Draw a pulsating vertical gradient across the entire screen."""
        t = pygame.time.get_ticks()
        pulse = (math.sin(t * 0.005) + 1) / 2
        top_color = [
            int(top_color_base[i] * (1 - pulse) + bottom_color_base[i] * pulse)
            for i in range(3)
        ]
        bottom_color = [
            int(bottom_color_base[i] * (1 - pulse) + top_color_base[i] * pulse)
            for i in range(3)
        ]
        for y in range(height):
            ratio = y / (height - 1)
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    @staticmethod
    def draw_settings_background(screen, width, height):
        """Blue-to-white vertical gradient for the settings panel."""
        for y in range(height):
            ratio = y / height
            r = int(30 + (220 - 30) * ratio)
            g = int(144 + (255 - 144) * ratio)
            b = 255
            pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    @staticmethod
    def draw_menu(screen, width, height, prompt, options,
                  title_font, option_font):
        """Centered title + selectable options on a translucent backdrop."""
        shadow = title_font.render(prompt, True, BLACK)
        title_surf = title_font.render(prompt, True, RED)
        title_w, _ = title_surf.get_size()
        screen.blit(shadow, ((width - title_w)//2 + 3, height//4 + 3))
        screen.blit(title_surf, ((width - title_w)//2, height//4))

        for text, color, pos_y in options:
            surf = option_font.render(text, True, color)
            rect = surf.get_rect(center=(width//2, pos_y))
            bg = pygame.Surface((rect.width + 20, rect.height + 10),
                                pygame.SRCALPHA)
            bg.fill((255, 255, 255, 100))
            screen.blit(bg, bg.get_rect(center=rect.center))
            screen.blit(surf, rect)

    # ------------------------------------------------------------------
    # In-game HUD
    # ------------------------------------------------------------------
    @staticmethod
    def show_score():
        """Render current left / right scores at top-left corner."""
        paddles = list(GlobalData.sprite_list)
        if len(paddles) != 2:
            return
        left_score = paddles[0].get_life()[0]
        right_score = paddles[1].get_life()[1]
        font = GameTextManager._get_font(50)
        score1 = font.render(f"Left: {left_score}", True, BLACK)
        score2 = font.render(f"Right: {right_score}", True, BLACK)
        GlobalData.screen.blit(score1, (20, 30))
        GlobalData.screen.blit(score2, (310, 30))

    @staticmethod
    def game_over_message(winner):
        """Black screen + winner text + restart prompt."""
        GlobalData.screen.fill((0, 0, 0))
        GameTextManager.draw_text(
            f"Game over: {winner} wins", 40, True, WHITE, 65, 200
        )
        GameTextManager.draw_text(
            "Press any key to play again", 25, True, RED, 120, 250, flip=True
        )

    # ------------------------------------------------------------------
    # Visual elements
    # ------------------------------------------------------------------
    @staticmethod
    def draw_center_line(color=RED):
        """Draw dashed centre line down the screen."""
        dash, gap = 20, 10
        for y in range(0, gHeight, dash + gap):
            start = (gWidth//2, y)
            end   = (gWidth//2, min(y + dash, gHeight))
            pygame.draw.line(GlobalData.screen, color, start, end, 4)

    @staticmethod
    def draw_button(rect, text, font_size, enabled):
        """Draw a rounded button with centered label; greyed when disabled."""
        color = pygame.Color("limegreen") if enabled else pygame.Color("gray50")
        pygame.draw.rect(GlobalData.screen, color, rect, border_radius=10)
        text_w = GameTextManager.font_width(text, font_size)
        x = rect.x + (rect.width - text_w)//2
        y = rect.y + (rect.height - font_size)//2
        GameTextManager.draw_text(text, font_size, True,
                                  pygame.Color("white"), x, y)

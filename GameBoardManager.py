import pygame
from constantsGlobal import gWidth, gHeight, WHITE, RED, GlobalData
from player import Player
from ball import Ball
from GameTextManager import GameTextManager


class GameBoardManager:
    """
    Handles everything drawn on the main game surface:
    * first screen upload (title + mode selection)
    * adding / resetting paddles and balls
    * full-frame redraws each tick, including score & glow
    """

    # --------------------------------------------------------
    # 1) First-time screen upload
    # --------------------------------------------------------
    @staticmethod
    def upload_screen(title, b_color, s_color):
        """Create the pygame window, clear it and draw the centre line."""
        pygame.init()
        GlobalData.screen = pygame.display.set_mode((gWidth, gHeight))
        pygame.display.set_caption(title)

        # delayed import – avoids circular dependency with pongGame.py
        from pongGame import againstWho
        GlobalData.against_com = againstWho()

        GameBoardManager.clear_screen(b_color)
        GameTextManager.draw_center_line(s_color)

    # --------------------------------------------------------
    # 2) Load or reset all sprites
    # --------------------------------------------------------
    @staticmethod
    def upload_sprites():
        """Erase old sprites, create fresh paddles & balls, then draw."""
        GlobalData.sprite_list.empty()
        GlobalData.ball_list.empty()

        left  = Player(0,               gHeight / 2, GlobalData.player_life)
        right = Player(gWidth - left.get_width(),
                       gHeight / 2, GlobalData.player_life)
        GlobalData.sprite_list.add(left, right)

        for _ in range(GlobalData.ball_amount):
            GlobalData.ball_list.add(Ball(gWidth / 2, gHeight / 2))

        GameBoardManager.redraw()      # first paint

    # --------------------------------------------------------
    # 3) Per-frame redraw (called by BallManager.r_screen)
    # --------------------------------------------------------
    @staticmethod
    def r_screen(b_color=WHITE, s_color=RED):
        """
        Repaint background, centre line, sprites, score and paddle glow.
        """
        GameBoardManager.clear_screen(b_color)
        GameTextManager.draw_center_line(s_color)
        GameBoardManager._draw_highlights()
        GameBoardManager.redraw()
        GameTextManager.show_score()
        pygame.display.flip()

    # --------------------------------------------------------
    # 4) Primitive helpers
    # --------------------------------------------------------
    @staticmethod
    def clear_screen(color):
        """Fill the entire window with a solid colour."""
        GlobalData.screen.fill(color)

    @staticmethod
    def redraw():
        """Blit every sprite group onto the screen."""
        GlobalData.sprite_list.draw(GlobalData.screen)
        GlobalData.ball_list.draw(GlobalData.screen)

    @staticmethod
    def _draw_highlights():
        """Glow overlay around each paddle for a subtle neon effect."""
        for paddle in GlobalData.sprite_list:
            rect = paddle.rect
            glow = pygame.Surface(
                (rect.width + 20, rect.height + 20), pygame.SRCALPHA
            )
            pygame.draw.rect(
                glow, (255, 255, 0, 60), glow.get_rect(), border_radius=10
            )
            GlobalData.screen.blit(glow, (rect.x - 10, rect.y - 10))

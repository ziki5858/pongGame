from constantsGlobal import *
from player import Player
from ball import Ball
from GameTextManager import GameTextManager

class GameBoardManager:
    @staticmethod
    def upload_screen(title, bColor, sColor):
        """Initialize Pygame screen and draw initial state."""
        pygame.init()
        GlobalData.screen = pygame.display.set_mode((gWidth, gHeight))
        pygame.display.set_caption(str(title))

        from pongGame import againstWho  # delayed import to avoid circular dependency
        GlobalData.against_com = againstWho()

        GameBoardManager.clear_screen(bColor)
        GameBoardManager.draw_center_line(sColor)

    @staticmethod
    def upload_sprites():
        """Clear existing sprites and add paddles and balls to sprite groups."""
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
        """Redraw entire game frame with highlights and score."""
        # redraw frame
        GameBoardManager.clear_screen(bColor)
        GameBoardManager.draw_center_line(sColor)
        # add ambient highlights
        GameBoardManager._draw_highlights()
        GameBoardManager.redraw()
        GameTextManager.show_score()
        pygame.display.flip()

    @staticmethod
    def clear_screen(color):
        """Fill background with specified color."""
        GlobalData.screen.fill(color)

    @staticmethod
    def draw_center_line(color):
        """Draw improved dashed center line."""
        dash_length = 20
        gap = 10
        for y in range(0, gHeight, dash_length + gap):
            start = (gWidth // 2, y)
            end = (gWidth // 2, min(y + dash_length, gHeight))
            pygame.draw.line(GlobalData.screen, color, start, end, 4)

    @staticmethod
    def redraw():
        """Render all sprites onto the screen."""
        GlobalData.sprite_list.draw(GlobalData.screen)
        GlobalData.ball_list.draw(GlobalData.screen)

    @staticmethod
    def _draw_highlights():
        """Draw simple glow effect around paddles only."""
        for paddle in GlobalData.sprite_list:
            rect = paddle.rect
            glow = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (255, 255, 0, 60), glow.get_rect(), border_radius=10)
            GlobalData.screen.blit(glow, (rect.x - 10, rect.y - 10))

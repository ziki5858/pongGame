import pygame
from game_sprite import GameSprite
from constantsGlobal import BLACK, gHeight


class Player(GameSprite):
    def __init__(self, x, y, life):
        super().__init__()
        self.image = pygame.image.load('sprite.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.get_height() / 2
        self.leftLife = life
        self.rightLife = life

    def constrain_y(self) -> None:
        """Keep the paddle inside the vertical screen bounds."""
        self.rect.y = max(0, min(self.rect.y, gHeight - self.rect.height))

    def clamp_y(self, y: float) -> float:
        """Return y limited to the screen’s vertical bounds."""
        return max(0, min(y, gHeight - self.rect.height))

    def lose_life(self, side):
        if side == 'left':
            self.leftLife -= 1
        elif side == 'right':
            self.rightLife -= 1

    def get_life(self):
        return self.leftLife, self.rightLife

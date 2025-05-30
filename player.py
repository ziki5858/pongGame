import pygame
from game_sprite import GameSprite
from constantsGlobal import BLACK, gHeight


class Player(GameSprite):
    """
    Paddle sprite: loads its own bitmap, keeps track of lives
    for both sides in two-player mode.
    """

    # --------------------------------------------------------
    # construction
    # --------------------------------------------------------
    def __init__(self, x, y, life):
        super().__init__()
        self.image = pygame.image.load("sprite.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.rect.height / 2       # centre on y

        self.leftLife  = life
        self.rightLife = life

    # --------------------------------------------------------
    # vertical limits
    # --------------------------------------------------------
    def constrain_y(self):
        """Snap the current rect.y inside the screen bounds."""
        self.rect.y = max(0, min(self.rect.y,
                                 gHeight - self.rect.height))

    def clamp_y(self, y):
        """Return y clamped to the legal vertical range."""
        return max(0, min(y, gHeight - self.rect.height))

    # --------------------------------------------------------
    # life handling
    # --------------------------------------------------------
    def lose_life(self, side):
        """Decrement life counter for the given side ('left' / 'right')."""
        if side == "left":
            self.leftLife -= 1
        elif side == "right":
            self.rightLife -= 1

    def get_life(self):
        """Return tuple (left_lives, right_lives)."""
        return self.leftLife, self.rightLife

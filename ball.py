import pygame, random
from game_sprite import GameSprite
from constantsGlobal import BLACK, BallSpeedPix

class Ball(GameSprite):
    _IMAGE = None  # cache

    def __init__(self, x, y, speed=BallSpeedPix):
        super().__init__()
        self.yMove = None
        self.xMove = None
        if Ball._IMAGE is None:
            img = pygame.image.load("ball.png").convert()
            img.set_colorkey(BLACK)
            Ball._IMAGE = img
        self.image = Ball._IMAGE
        self.rect  = self.image.get_rect(center=(x, y))
        self.speed = speed
        self._randomize_velocity()

    # --- public API -------------------------------------------------
    def update_Move(self, vx, vy):
        self.xMove, self.yMove = vx, vy

    def get_move(self):
        return self.xMove, self.yMove

    def reset_position(self, x, y):
        self.rect.center = (x, y)
        self._randomize_velocity()

    # --- internal helpers -------------------------------------------
    def _randomize_velocity(self):
        self.xMove = random.choice([-1, 1]) * self.speed
        self.yMove = random.choice([-1, 1]) * self.speed

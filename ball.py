import pygame
import random
from game_sprite import GameSprite
from constantsGlobal import BLACK, BallSpeedPix

class Ball(GameSprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('ball.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Randomize initial movement direction
        self.xMove = random.choice([-1, 1]) * BallSpeedPix
        self.yMove = random.choice([-1, 1]) * BallSpeedPix

    def update_Move(self, x, y):
        self.xMove = x
        self.yMove = y

    def get_move(self):
        return self.xMove, self.yMove

    def reset_position(self, x, y):
        self.rect.center = (x, y)
        # Randomize direction on reset as well
        self.xMove = random.choice([-1, 1]) * BallSpeedPix
        self.yMove = random.choice([-1, 1]) * BallSpeedPix

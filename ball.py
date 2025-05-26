import pygame
from game_sprite import GameSprite
from constants import BLACK, BallSpeedPix

class Ball(GameSprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('ball.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.xMove = BallSpeedPix
        self.yMove = -BallSpeedPix

    def update_Move(self, x, y):
        self.xMove = x
        self.yMove = y

    def get_move(self):
        return self.xMove, self.yMove

    def reset_position(self, x, y):
        self.rect.center = (x, y)
        self.xMove = BallSpeedPix
        self.yMove = -BallSpeedPix

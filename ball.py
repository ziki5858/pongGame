import pygame
from game_sprite import GameSprite
from constants import BLACK, BallSpeedPix

class Ball(GameSprite):
    def __init__(self, x, y):
        super(Ball, self).__init__()
        self.image = pygame.image.load('ball.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.get_width() / 2
        self.rect.y = y - self.get_height() / 2
        self.xMOve = BallSpeedPix
        self.yMove = -BallSpeedPix

    def update_Move(self, x, y):
        self.xMOve = x
        self.yMove = y

    def get_move(self):
        return self.xMOve, self.yMove

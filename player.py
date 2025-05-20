# player.py
import pygame
from game_sprite import GameSprite
from constants import BLACK, LIFE

class Player(GameSprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprite.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.get_height() / 2
        self.leftLife = LIFE
        self.rightLife = LIFE

    def update_left_Life(self):
        self.leftLife -= 1

    def update_right_Life(self):
        self.rightLife -= 1

    def get_life(self):
        return self.leftLife, self.rightLife

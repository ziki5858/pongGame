import pygame

class GameSprite(pygame.sprite.Sprite):
    def update_loc(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_pos(self):
        return self.rect.x, self.rect.y

    def get_posX(self):
        return self.rect.x

    def get_posY(self):
        return self.rect.y

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

import pygame

screen = None
against_com = False
sprite_list = pygame.sprite.Group()
ball_list = pygame.sprite.Group()

# User-defined settings (set via game_settings)
ball_amount = 1         # default 1 ball
player_life = 2         # default 2 lives
com_level = 15          # default medium AI

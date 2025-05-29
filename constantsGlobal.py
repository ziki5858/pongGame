# constantsGlobal.py
import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen
gWidth, gHeight = 500, 500
REFRESH         = 60

# Ball
BallSpeedPix   = 1.9
AddSpeedBall   = 0.1
BALL_AMOUNT    = 1

# Game
LIFE        = 2
Xdeviation  = 15
COM_LEVEL   = 15  # medium AI difficulty

class GlobalData:
    """
    Holds global game state and user-defined settings.
    Access these attributes via GlobalData.<attribute>.
    """
    # Pygame display surface
    screen: pygame.Surface = None

    # Game mode flags
    against_com: bool = False

    # Sprite groups
    sprite_list: pygame.sprite.Group = pygame.sprite.Group()
    ball_list: pygame.sprite.Group = pygame.sprite.Group()

    # User-defined settings (set via game_settings)
    ball_amount: int = 1     # default 1 ball
    player_life: int = 2     # default 2 lives
    com_level: int = 15      # default medium AI

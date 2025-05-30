# constantsGlobal.py
# ------------------------------------------------------------
# Central place for immutable “tuning knobs” and runtime state
# ------------------------------------------------------------
import pygame

# ------------------------------------------------------------
# Basic Colors (RGB)
# ------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# ------------------------------------------------------------
# Screen configuration
# ------------------------------------------------------------
gWidth, gHeight = 500, 500        # window size (px)
REFRESH         = 60              # FPS cap

# ------------------------------------------------------------
# Ball physics defaults
# ------------------------------------------------------------
BallSpeedPix = 1.9    # base velocity (px / frame)
AddSpeedBall = 0.1    # speed added after each paddle hit
BALL_AMOUNT  = 1      # default number of balls

# ------------------------------------------------------------
# Game-play constants
# ------------------------------------------------------------
LIFE       = 2        # starting lives per paddle
Xdeviation = 15       # horizontal leeway for paddle collision
COM_LEVEL  = 15       # medium AI difficulty

# ------------------------------------------------------------
# Runtime state container
# ------------------------------------------------------------
class GlobalData:
    """
    Holds mutable game state and user-defined settings.
    Access via `GlobalData.<attribute>` from anywhere.

    NOTE
    ----
    * `screen` is assigned once in main() right after pygame.init().
    * `sprite_list` / `ball_list` are cleared on every new game.
    * All other fields may be changed by menus or game logic.
    """
    # Pygame display surface (set in main)
    screen: pygame.Surface | None = None

    # Game-mode flag
    against_com: bool = False

    # Sprite groups
    sprite_list: pygame.sprite.Group = pygame.sprite.Group()
    ball_list:   pygame.sprite.Group = pygame.sprite.Group()

    # User-selected settings (overwritten in settings panel)
    ball_amount: int = BALL_AMOUNT
    player_life: int = LIFE
    com_level:   int = COM_LEVEL

    # --------------------------------------------------------
    # Helper utilities
    # --------------------------------------------------------
    @staticmethod
    def reset() :
        """
        Clear runtime collections & mode flags
        before starting a fresh match.
        """
        GlobalData.sprite_list.empty()
        GlobalData.ball_list.empty()
        GlobalData.against_com = False

    @staticmethod
    def dump():
        """Print current state (handy for quick debug)."""
        public = {k: v for k, v in vars(GlobalData).items()
                  if not k.startswith('__')}
        for k, v in public.items():
            print(f"{k:12} → {v}")

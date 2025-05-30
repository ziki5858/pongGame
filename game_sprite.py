import pygame
from typing import Tuple


class GameSprite(pygame.sprite.Sprite):
    """
    Base class for all game objects that own a pygame.Rect.
    Provides minimal helpers for absolute positioning and sizing.
    """

    # ---------------------- Public API ---------------------- #
    def update_loc(self, x: float, y: float) -> None:
        """Move the sprite’s rect to the exact (x, y) position."""
        self.rect.x = x
        self.rect.y = y

    def get_pos(self) -> Tuple[float, float]:
        """Return current (x, y) coordinates of the sprite."""
        return self.rect.x, self.rect.y

    def get_posX(self) -> float:
        """Return only the x-coordinate."""
        return self.rect.x

    def get_posY(self) -> float:
        """Return only the y-coordinate."""
        return self.rect.y

    def get_width(self) -> int:
        """Return the rect’s width in pixels."""
        return self.rect.width

    def get_height(self) -> int:
        """Return the rect’s height in pixels."""
        return self.rect.height

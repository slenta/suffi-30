"""
Base sprite classes for consistent sprite initialization.
"""

import pygame as pg
from .settings import GRIDSIZE


class GridSprite(pg.sprite.Sprite):
    """Base class for sprites that use grid-based positioning."""

    def __init__(self, x, y, image, convert_to_grid=True):
        """
        Initialize a grid-based sprite.

        Args:
            x: X position (grid units if convert_to_grid=True, pixels otherwise)
            y: Y position (grid units if convert_to_grid=True, pixels otherwise)
            image: Pygame surface for the sprite
            convert_to_grid: If True, convert x,y from grid to pixels
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

        if convert_to_grid:
            self.rect.x = x * GRIDSIZE
            self.rect.y = y * GRIDSIZE
        else:
            self.rect.x = x
            self.rect.y = y


class CollectibleSprite(GridSprite):
    """Base class for collectible items (gems, power-ups, etc.)."""

    def __init__(self, x, y, image, convert_to_grid=True):
        super().__init__(x, y, image, convert_to_grid)

    def apply(self, character):
        """
        Apply the collectible's effect to a character.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement apply()")

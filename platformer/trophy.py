"""Trophy and exit door sprites."""

import pygame as pg
import os
from .settings import IMAGEPATH, GRIDSIZE


class Trophy(pg.sprite.Sprite):
    """Collectible trophy sprite."""

    def __init__(self, x, y, image_path="trophy.png"):
        """
        Initialize a trophy.

        Args:
            x: X position in pixels
            y: Y position in pixels
            image_path: Path to trophy image relative to IMAGEPATH
        """
        super().__init__()
        image = pg.image.load(os.path.join(IMAGEPATH, image_path)).convert_alpha()
        self.image = pg.transform.scale(image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pg.sprite.Sprite):
    """Level exit door that opens when all trophies are collected."""

    def __init__(self, x, y):
        """
        Initialize an exit door.

        Args:
            x: X position in pixels
            y: Y position in pixels
        """
        super().__init__()
        self.closed_image = pg.image.load(
            os.path.join(IMAGEPATH, "door_closed.png")
        ).convert_alpha()
        self.open_image = pg.image.load(
            os.path.join(IMAGEPATH, "door_open.png")
        ).convert_alpha()
        self.image = pg.transform.scale(self.closed_image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_open = False

    def open(self):
        """Open the exit door."""
        self.image = pg.transform.scale(self.open_image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.is_open = True

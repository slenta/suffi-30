"""Trophy and exit door sprites."""

import pygame as pg
import os
from ..config.settings import IMAGEPATH, GRIDSIZE


class Trophy(pg.sprite.Sprite):
    """Collectible trophy sprite."""

    def __init__(self, x, y, image_path="trophy.png", trophy_id=None):
        """
        Initialize a trophy.

        Args:
            x: X position in pixels
            y: Y position in pixels
            image_path: Path to trophy image relative to IMAGEPATH
            trophy_id: Unique identifier for tracking collection state
        """
        super().__init__()
        image = pg.image.load(os.path.join(IMAGEPATH, image_path)).convert_alpha()
        self.image = pg.transform.scale(image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.trophy_id = trophy_id  # Store ID for tracking


class Exit(pg.sprite.Sprite):
    """Level exit door that opens when all trophies are collected."""

    def __init__(
        self,
        x,
        y,
        closed_image="door_closed.png",
        open_image="door_open.png",
        size_multiplier=2,
    ):
        """
        Initialize an exit door.

        Args:
            x: X position in pixels
            y: Y position in pixels
            closed_image: Path to closed door image relative to IMAGEPATH
            open_image: Path to open door image relative to IMAGEPATH
            size_multiplier: Multiplier for exit door size (default: 2)
        """
        super().__init__()
        self.size_multiplier = size_multiplier
        self.closed_image = pg.image.load(
            os.path.join(IMAGEPATH, closed_image)
        ).convert_alpha()
        self.open_image = pg.image.load(
            os.path.join(IMAGEPATH, open_image)
        ).convert_alpha()
        exit_size = int(size_multiplier * GRIDSIZE)
        self.image = pg.transform.scale(self.closed_image, (exit_size, exit_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_open = False

    def open(self):
        """Open the exit door."""
        exit_size = int(self.size_multiplier * GRIDSIZE)
        self.image = pg.transform.scale(self.open_image, (exit_size, exit_size))
        self.is_open = True

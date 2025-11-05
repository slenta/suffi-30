"""Platform sprite class."""

import pygame as pg
from ..core.base_sprites import GridSprite


class Platform(GridSprite):
    """Static platform sprite."""

    def __init__(self, x, y, image):
        """
        Initialize a platform.

        Args:
            x: X position in grid units
            y: Y position in grid units
            image: Platform image surface
        """
        super().__init__(x, y, image, convert_to_grid=True)

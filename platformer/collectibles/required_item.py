"""Required items that must be collected to complete a level (e.g., keys, tickets)."""

import pygame as pg
import os
from ..config.settings import IMAGEPATH, GRIDSIZE


class RequiredItem(pg.sprite.Sprite):
    """A required item that must be collected to open the exit (like a key or ticket)."""

    def __init__(self, x, y, item_id, image_path="key.png"):
        """
        Initialize a required item.

        Args:
            x: X position in pixels
            y: Y position in pixels
            item_id: Unique identifier for this item (e.g., "busticket")
            image_path: Path to item image relative to IMAGEPATH
        """
        super().__init__()
        image = pg.image.load(os.path.join(IMAGEPATH, image_path)).convert_alpha()
        self.image = pg.transform.scale(image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.item_id = item_id  # Unique ID for tracking

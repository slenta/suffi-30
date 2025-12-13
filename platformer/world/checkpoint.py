"""Checkpoint system for respawning at saved positions."""

import pygame as pg
import os
from ..config.settings import IMAGEPATH, GRIDSIZE


class Checkpoint(pg.sprite.Sprite):
    """Checkpoint that saves player progress and respawn position."""

    def __init__(self, x, y, image_path="checkpoint.png"):
        """
        Initialize a checkpoint.

        Args:
            x: X position in grid units
            y: Y position in grid units
            image_path: Path to checkpoint image relative to IMAGEPATH
        """
        super().__init__()
        
        # Load and scale the checkpoint image
        try:
            image = pg.image.load(os.path.join(IMAGEPATH, image_path)).convert_alpha()
        except:
            # Fallback: create a simple colored rectangle if image doesn't exist
            image = pg.Surface((GRIDSIZE * 2, GRIDSIZE * 3), pg.SRCALPHA)
            pg.draw.rect(image, (0, 255, 0), image.get_rect(), 3)
            pg.draw.circle(image, (0, 255, 0), (GRIDSIZE, GRIDSIZE), GRIDSIZE // 2)
        
        self.image = pg.transform.scale(image, (GRIDSIZE * 2, GRIDSIZE * 3))
        self.rect = self.image.get_rect()
        self.rect.x = x * GRIDSIZE
        self.rect.bottom = y * GRIDSIZE
        
        # Checkpoint state
        self.activated = False
        self.original_image = self.image.copy()
        
        # Store spawn position (in grid units for consistency)
        self.spawn_x = x
        self.spawn_y = y

    def activate(self):
        """Activate the checkpoint (visual feedback)."""
        if not self.activated:
            self.activated = True
            # Change appearance when activated (e.g., brighten or change color)
            self.image = self.original_image.copy()
            # Add a green overlay to show it's active
            overlay = pg.Surface(self.image.get_size(), pg.SRCALPHA)
            overlay.fill((0, 255, 0, 100))
            self.image.blit(overlay, (0, 0))

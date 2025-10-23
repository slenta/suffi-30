"""
Pipe class for entering sub-levels (similar to Mario green pipes).
"""

import pygame as pg
import os
from .settings import IMAGEPATH, GRIDSIZE


class Pipe(pg.sprite.Sprite):
    """A pipe that allows the player to enter a sub-level."""

    def __init__(
        self, x, y, sub_level_name, return_x=None, return_y=None, direction="down"
    ):
        """
        Initialize a pipe.

        Args:
            x: X position in pixels
            y: Y position in pixels
            sub_level_name: Name of the sub-level to load (e.g., "sub-underwater")
            return_x: X position (grid units) where player spawns when returning (optional)
            return_y: Y position (grid units) where player spawns when returning (optional)
            direction: Direction of pipe entrance ("down", "up", "left", "right")
        """
        super().__init__()

        # Load pipe image
        pipe_image_path = os.path.join(IMAGEPATH, "pipe", "pipe.png")
        try:
            pipe_image = pg.image.load(pipe_image_path).convert_alpha()
        except (pg.error, FileNotFoundError):
            # Fallback to door image if pipe image doesn't exist
            print(f"⚠️ Pipe image not found at {pipe_image_path}, using fallback")
            pipe_image = pg.image.load(
                os.path.join(IMAGEPATH, "door_closed.png")
            ).convert_alpha()

        self.image = pg.transform.scale(pipe_image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.sub_level_name = sub_level_name
        self.return_x = return_x
        self.return_y = return_y
        self.direction = direction
        self.is_active = True

        # Cooldown to prevent immediate re-entry
        self.entry_cooldown = 0

    def can_enter(self, player, keys):
        """Check if the player can enter the pipe."""
        if not self.is_active or self.entry_cooldown > 0:
            return False

        # Check if player is colliding with pipe
        if not pg.sprite.collide_rect(player, self):
            return False

        # Check if correct key is pressed based on direction
        if self.direction == "down":
            return keys[pg.K_DOWN] or keys[pg.K_s]
        elif self.direction == "up":
            return keys[pg.K_UP] or keys[pg.K_w]
        elif self.direction == "left":
            return keys[pg.K_LEFT] or keys[pg.K_a]
        elif self.direction == "right":
            return keys[pg.K_RIGHT] or keys[pg.K_d]

        return False

    def update(self):
        """Update pipe state."""
        if self.entry_cooldown > 0:
            self.entry_cooldown -= 1

    def reset_cooldown(self):
        """Reset the entry cooldown (30 frames = 0.5 seconds at 60 FPS)."""
        self.entry_cooldown = 30

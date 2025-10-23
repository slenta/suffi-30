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
            x: X position of pipe (grid units)
            y: Y position of pipe (pixels)
            image: Pygame surface for the pipe
            sub_level_name: Name of the sub-level to load (e.g., "underwater-sub")
            return_x: X position to spawn player when returning from sub-level (grid units)
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
        self.rect.x = x
        self.rect.y = y

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

        # Check if player is colliding with pipe OR standing on top of it
        is_colliding = pg.sprite.collide_rect(player, self)

        # Also check if player is standing on top of the pipe (for "down" direction)
        is_on_top = False
        if self.direction == "down":
            # Check if player's bottom is near the pipe's top and they overlap horizontally
            player_bottom = player.rect.bottom
            pipe_top = self.rect.top
            # Allow some tolerance (within 5 pixels)
            if abs(player_bottom - pipe_top) <= 5:
                # Check horizontal overlap
                if (
                    player.rect.right > self.rect.left
                    and player.rect.left < self.rect.right
                ):
                    is_on_top = True

        # Debug: Print positions when player is near
        if abs(player.rect.x - self.rect.x) < 100:
            print(
                f"🔍 Player at ({player.rect.x}, {player.rect.y}), size: {player.rect.width}x{player.rect.height}"
            )
            print(
                f"🔍 Pipe at ({self.rect.x}, {self.rect.y}), size: {self.rect.width}x{self.rect.height}"
            )
            print(f"🔍 Collision: {is_colliding}, On Top: {is_on_top}")

        if not (is_colliding or is_on_top):
            return False

        # Check if correct key is pressed based on direction
        key_pressed = False
        if self.direction == "down":
            key_pressed = keys[pg.K_DOWN] or keys[pg.K_s]
        elif self.direction == "up":
            key_pressed = keys[pg.K_UP] or keys[pg.K_w]
        elif self.direction == "left":
            key_pressed = keys[pg.K_LEFT] or keys[pg.K_a]
        elif self.direction == "right":
            key_pressed = keys[pg.K_RIGHT] or keys[pg.K_d]

        if is_colliding or is_on_top:
            print(
                f"🚪 Player near pipe! Key pressed: {key_pressed}, Direction: {self.direction}"
            )

        return key_pressed

    def update(self):
        """Update pipe state."""
        if self.entry_cooldown > 0:
            self.entry_cooldown -= 1

    def reset_cooldown(self):
        """Reset the entry cooldown (30 frames = 0.5 seconds at 60 FPS)."""
        self.entry_cooldown = 30

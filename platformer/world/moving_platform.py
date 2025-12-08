import pygame as pg
from ..config.settings import *


class MovingPlatform(pg.sprite.Sprite):
    """A platform that moves between two points."""

    def __init__(
        self, _x, _y, _image, movement_type, speed, distance, direction="horizontal"
    ):
        """
        Initialize a moving platform.

        Args:
            _x: Starting x grid position
            _y: Starting y grid position
            _image: Platform image
            movement_type: "linear" or "circular"
            speed: Movement speed in pixels per frame
            distance: Distance to travel (in grid units for linear, radius for circular)
            direction: "horizontal" or "vertical" (for linear movement only)
        """
        super().__init__()
        self.image = _image
        self.rect = self.image.get_rect()
        self.start_x = _x * GRIDSIZE
        self.start_y = _y * GRIDSIZE
        self.rect.x = self.start_x
        self.rect.y = self.start_y

        self.movement_type = movement_type
        self.speed = speed
        self.distance = distance * GRIDSIZE  # Convert grid units to pixels
        self.direction = direction

        # For linear movement
        self.moving_forward = True
        self.current_distance = 0

        # For circular movement: use the sprite center as the rotation center
        self.angle = 0
        self.center_x = self.start_x + self.rect.width // 2
        self.center_y = self.start_y + self.rect.height // 2

        # Store previous position for player movement
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y

    def update(self):
        """Update the platform's position."""
        # Store previous position
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y

        if self.movement_type == "linear":
            self._update_linear()
        elif self.movement_type == "circular":
            self._update_circular()

    def _update_linear(self):
        """Update linear movement (back and forth)."""
        if self.direction == "horizontal":
            if self.moving_forward:
                self.rect.x += self.speed
                self.current_distance += self.speed
                if self.current_distance >= self.distance:
                    self.moving_forward = False
            else:
                self.rect.x -= self.speed
                self.current_distance -= self.speed
                if self.current_distance <= 0:
                    self.moving_forward = True

        elif self.direction == "vertical":
            if self.moving_forward:
                self.rect.y += self.speed
                self.current_distance += self.speed
                if self.current_distance >= self.distance:
                    self.moving_forward = False
            else:
                self.rect.y -= self.speed
                self.current_distance -= self.speed
                if self.current_distance <= 0:
                    self.moving_forward = True

    def _update_circular(self):
        """Update circular movement."""
        # Increase angular speed multiplier so circular platforms are visibly moving
        # Treat `speed` as an abstract speed factor (degrees per frame multiplier)
        self.angle += self.speed * 3.0
        radius = self.distance  # Already in pixels

        vec = pg.math.Vector2(1, 0).rotate(self.angle)
        # Position the platform so its center follows the circular path
        self.rect.x = int(self.center_x + radius * vec.x - self.rect.width // 2)
        self.rect.y = int(self.center_y + radius * vec.y - self.rect.height // 2)

    def get_velocity(self):
        """Get the platform's velocity for player movement."""
        vel_x = self.rect.x - self.prev_x
        vel_y = self.rect.y - self.prev_y
        return vel_x, vel_y


## End Class MovingPlatform

import pygame as pg
from .settings import *


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

        # For circular movement
        self.angle = 0
        self.center_x = self.start_x
        self.center_y = self.start_y

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
        self.angle += self.speed * 0.02  # Adjust rotation speed
        radius = self.distance  # Use distance as radius

        self.rect.x = int(
            self.center_x + radius * pg.math.Vector2(1, 0).rotate(self.angle).x
        )
        self.rect.y = int(
            self.center_y + radius * pg.math.Vector2(1, 0).rotate(self.angle).y
        )

    def get_velocity(self):
        """Get the platform's velocity for player movement."""
        vel_x = self.rect.x - self.prev_x
        vel_y = self.rect.y - self.prev_y
        return vel_x, vel_y


## End Class MovingPlatform

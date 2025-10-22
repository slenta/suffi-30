import pygame as pg
from .settings import *


class Spike(pg.sprite.Sprite):
    """
    Spike block that damages the player on collision.
    Can face four directions: up, down, left, right
    """

    def __init__(self, x, y, direction="up", damage=10):
        """
        Initialize a spike block.

        Args:
            x: Grid x position
            y: Grid y position
            direction: Direction spikes point ("up", "down", "left", "right")
            damage: Amount of damage dealt to player
        """
        super().__init__()
        self.direction = direction
        self.damage = damage

        # Create spike image based on direction
        self.image = self.create_spike_image()
        self.rect = self.image.get_rect()
        self.rect.x = x * GRIDSIZE
        self.rect.y = y * GRIDSIZE

        # Create smaller hitbox for the actual spikes (not the base)
        self.damage_rect = self.get_damage_rect()

    def create_spike_image(self):
        """Create a spike block image based on direction"""
        surface = pg.Surface((GRIDSIZE, GRIDSIZE), pg.SRCALPHA)

        # Base color (dark gray)
        base_color = (60, 60, 60)
        # Spike color (lighter gray with red tint)
        spike_color = (150, 50, 50)

        if self.direction == "up":
            # Draw base at bottom
            pg.draw.rect(
                surface, base_color, (0, GRIDSIZE * 0.7, GRIDSIZE, GRIDSIZE * 0.3)
            )
            # Draw spikes pointing up
            spike_width = GRIDSIZE // 5
            for i in range(5):
                x = i * spike_width
                points = [
                    (x, GRIDSIZE * 0.7),
                    (x + spike_width // 2, 0),
                    (x + spike_width, GRIDSIZE * 0.7),
                ]
                pg.draw.polygon(surface, spike_color, points)

        elif self.direction == "down":
            # Draw base at top
            pg.draw.rect(surface, base_color, (0, 0, GRIDSIZE, GRIDSIZE * 0.3))
            # Draw spikes pointing down
            spike_width = GRIDSIZE // 5
            for i in range(5):
                x = i * spike_width
                points = [
                    (x, GRIDSIZE * 0.3),
                    (x + spike_width // 2, GRIDSIZE),
                    (x + spike_width, GRIDSIZE * 0.3),
                ]
                pg.draw.polygon(surface, spike_color, points)

        elif self.direction == "left":
            # Draw base on right
            pg.draw.rect(
                surface, base_color, (GRIDSIZE * 0.7, 0, GRIDSIZE * 0.3, GRIDSIZE)
            )
            # Draw spikes pointing left
            spike_height = GRIDSIZE // 5
            for i in range(5):
                y = i * spike_height
                points = [
                    (GRIDSIZE * 0.7, y),
                    (0, y + spike_height // 2),
                    (GRIDSIZE * 0.7, y + spike_height),
                ]
                pg.draw.polygon(surface, spike_color, points)

        elif self.direction == "right":
            # Draw base on left
            pg.draw.rect(surface, base_color, (0, 0, GRIDSIZE * 0.3, GRIDSIZE))
            # Draw spikes pointing right
            spike_height = GRIDSIZE // 5
            for i in range(5):
                y = i * spike_height
                points = [
                    (GRIDSIZE * 0.3, y),
                    (GRIDSIZE, y + spike_height // 2),
                    (GRIDSIZE * 0.3, y + spike_height),
                ]
                pg.draw.polygon(surface, spike_color, points)

        return surface

    def get_damage_rect(self):
        """Get the actual damage hitbox for the spikes (smaller than full block)"""
        damage_rect = self.rect.copy()

        # Make the damage area smaller based on spike direction
        shrink = GRIDSIZE // 4

        if self.direction == "up":
            damage_rect.top += shrink
            damage_rect.height -= shrink
        elif self.direction == "down":
            damage_rect.height -= shrink
        elif self.direction == "left":
            damage_rect.left += shrink
            damage_rect.width -= shrink
        elif self.direction == "right":
            damage_rect.width -= shrink

        return damage_rect

    def update(self):
        """Update damage rect position"""
        self.damage_rect = self.get_damage_rect()

    def check_collision(self, player):
        """
        Check if player collides with the spike's damage area.

        Args:
            player: Player sprite to check collision with

        Returns:
            bool: True if collision detected
        """
        return self.damage_rect.colliderect(player.rect)

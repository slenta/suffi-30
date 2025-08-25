import pygame as pg
import os
from .settings import IMAGEPATH, GRIDSIZE  # Ensure GRIDSIZE and IMAGEPATH are imported


class PowerUp(pg.sprite.Sprite):
    def __init__(self, x, y, power_type, world):
        super().__init__()
        self.world = world
        self.power_type = power_type

        # Load custom images for each power-up type
        if power_type == 0:
            image = pg.image.load(os.path.join(IMAGEPATH, "banana.png")).convert_alpha()
        elif power_type == 1:
            image = pg.image.load(os.path.join(IMAGEPATH, "pulver.png")).convert_alpha()
        else:
            image = pg.Surface((20, 20))  # Default size for unknown power-ups
            image.fill((255, 255, 0))  # Yellow for unknown power-ups

        # Scale the image to the grid size
        self.image = pg.transform.scale(image, (GRIDSIZE, GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def apply_effect(self, player):
        if self.power_type == 0:
            # Make the player bigger
            player.image = pg.transform.scale(
                player.image, (player.rect.width * 2, player.rect.height * 2)
            )
            player.rect = player.image.get_rect(center=player.rect.center)
        elif self.power_type == 1:
            # Make the player faster
            player.speed += 4  # Increase player's speed

    def power_down(self, player):
        if self.power_type == 0:
            # Restore normal size (assuming player.normal_size exists)
            player.image = pg.transform.scale(
                player.image, (player.rect.width // 2, player.rect.height // 2)
            )
            player.rect = player.image.get_rect(center=player.rect.center)
        elif self.power_type == 1:
            # Restore normal speed (assuming player.normal_speed exists)
            player.speed -= 4

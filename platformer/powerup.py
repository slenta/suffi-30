import pygame as pg
import os
from .settings import IMAGEPATH, GRIDSIZE  # Ensure GRIDSIZE and IMAGEPATH are imported


class PowerUp(pg.sprite.Sprite):
    def __init__(self, x, y, power_type, world):
        super().__init__()
        self.world = world
        self.power_type = power_type

        # Load custom images for each power-up type
        if power_type == "bigger":
            image = pg.image.load(os.path.join(IMAGEPATH, "banana.png")).convert_alpha()
        elif power_type == "faster":
            image = pg.image.load(os.path.join(IMAGEPATH, "pulver.png")).convert_alpha()
        elif power_type == "no_gravity":
            image = pg.image.load(
                os.path.join(IMAGEPATH, "redbull.jpeg")
            ).convert_alpha()
        else:
            image = pg.Surface((20, 20))  # Default size for unknown power-ups
            image.fill((255, 255, 0))  # Yellow for unknown power-ups

        # Scale the image to the grid size
        self.image = pg.transform.scale(image, (GRIDSIZE, GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def apply_effect(self, player):
        if self.power_type == "bigger":
            # Make the player bigger
            player.image = pg.transform.scale(
                player.image, (player.rect.width * 2, player.rect.height * 2)
            )
            player.rect = player.image.get_rect(center=player.rect.center)
        elif self.power_type == "faster":
            # Make the player faster
            player.speed += 4  # Increase player's speed
        elif self.power_type == "no_gravity":
            # Disable gravity for the player
            player.disable_gravity(
                300
            )  # Disable gravity for 300 frames (5 seconds at 60 FPS)

    def power_down(self, player):
        if self.power_type == "bigger":
            # Restore normal size (assuming player.normal_size exists)
            player.image = pg.transform.scale(player.image, player.normal_size)
            player.rect = player.image.get_rect(center=player.rect.center)
        elif self.power_type == "faster":
            # Restore normal speed (assuming player.normal_speed exists)
            player.speed = player.normal_speed
        elif self.power_type == "no_gravity":
            # Restore gravity (assuming player.enable_gravity exists)
            player.enable_gravity()

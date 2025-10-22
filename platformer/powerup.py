import pygame as pg
import os
import random
from .settings import IMAGEPATH, GRIDSIZE  # Ensure GRIDSIZE and IMAGSIZE are imported


class PowerUp(pg.sprite.Sprite):
    """
    PowerUp class for different power-up types in the game.

    Power-up types:
    - Type 0: Makes the player bigger (banana.png)
    - Type 1: Makes the player faster (pulver.png)
    - Type 2: Changes the level background (spraydose.png)
    - Type 3: Chaos effect - reverses left/right controls, increases speed by 6, and has 50% chance to set FPS to 10 for 8 seconds

    To use type 2 (background changer):
    1. Add a power-up in your level config:
       {"x": 50, "y": 10, "type": 2}

    2. Add alternative backgrounds in your level config:
       "alternative_backgrounds": [
           "assets/backgrounds/level2.png",
           "assets/backgrounds/level3.png"
       ]

    The power-up will cycle through all alternative backgrounds and back to the original.
    """

    def __init__(self, x, y, power_type, world):
        super().__init__()
        self.world = world
        self.power_type = power_type
        self.fps_changed = False  # Track if FPS was changed for type 3
        self.speed_changed = False  # Track if speed was changed for type 3

        # Load custom images for each power-up type
        if power_type == 0:
            image = pg.image.load(os.path.join(IMAGEPATH, "banana.png")).convert_alpha()
        elif power_type == 1:
            image = pg.image.load(os.path.join(IMAGEPATH, "pulver.png")).convert_alpha()
        elif power_type == 2:
            image = pg.image.load(
                os.path.join(IMAGEPATH, "powerups/powerup-pill.png")
            ).convert_alpha()
        elif power_type == 3:
            image = pg.image.load(os.path.join(IMAGEPATH, "pulver.png")).convert_alpha()
        else:
            image = pg.Surface((20, 20))  # Default size for unknown power-ups
            image.fill((255, 255, 0))  # Yellow for unknown power-ups

        # Scale the image to the grid size
        self.image = pg.transform.scale(image, (2 * GRIDSIZE, 2 * GRIDSIZE))
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
        elif self.power_type == 2:
            # Change the background
            self.world.change_background()
        elif self.power_type == 3:
            # Chaos effect - 50% chance for one of two effects
            if random.random() < 0.5:
                # Option A: Reverse controls + slow FPS
                player.controls_reversed = True
                self.world.set_fps(10)
                self.fps_changed = True
                self.speed_changed = False
            else:
                # Option B: Speed increase
                player.speed += 6
                self.speed_changed = True
                self.fps_changed = False

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
        elif self.power_type == 3:
            # Restore effects based on what was activated
            if self.fps_changed:
                # Was Option A: restore controls and FPS
                player.controls_reversed = False
                self.world.reset_fps()
            if self.speed_changed:
                # Was Option B: restore speed
                player.speed -= 6

"""Power-up collectibles with various effects."""

import pygame as pg
import os
import random
from ..config.settings import IMAGEPATH, GRIDSIZE
from ..config.constants import (
    POWERUP_SPEED_INCREASE,
    POWERUP_CHAOS_SPEED_INCREASE,
    POWERUP_CHAOS_FPS,
    POWERUP_SIZE_MULTIPLIER,
)
from ..config.constants import (
    POWERUP_FLY_DURATION,
    POWERUP_FLY_SPEED_PENALTY,
    POWERUP_JOINT_PIXELATION_FACTOR,
)


class PowerUp(pg.sprite.Sprite):
    """
    PowerUp class for different power-up types in the game.

    Power-up types:
    - Type 0: Makes the player bigger (banana.png)
    - Type 1: Makes the player faster (pulver.png)
    - Type 2: Changes the level background (spraydose.png)
    - Type 3: Chaos effect - reverses left/right controls, increases speed by 6, and has 50% chance to set FPS to 10 for 8 seconds
    - Type 4: Makes the player bigger (babybrei.png)
        - Type 5: Teil - Creates pixelation/rasterization effect for 15 seconds
            - Type 6: Joint - Applies a very strong pixelation effect and a larger
                immediate speed penalty, and grants flight instantly. The effect lasts
                7 seconds total.

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
        # Track whether this powerup applied a flight speed penalty so we can restore correctly
        self._applied_fly_penalty = False

        # Load custom images for each power-up type
        if power_type == 0:
            image = pg.image.load(os.path.join(IMAGEPATH, "banana.png")).convert_alpha()
        elif power_type == 1:
            image = pg.image.load(
                os.path.join(IMAGEPATH, "powerups/pulver.png")
            ).convert_alpha()
        elif power_type == 2:
            image = pg.image.load(
                os.path.join(IMAGEPATH, "powerups/powerup-pill.png")
            ).convert_alpha()
        elif power_type == 3:
            image = pg.image.load(
                os.path.join(IMAGEPATH, "powerups/pulver.png")
            ).convert_alpha()
        elif power_type == 4:
            image = pg.image.load(
                os.path.join(IMAGEPATH, "powerups/babybrei.png")
            ).convert_alpha()
        elif power_type == 5:
            # Teil powerup - radial blur effect
            image = pg.image.load(
                os.path.join(IMAGEPATH, "powerups/teil.png")
            ).convert_alpha()
        elif power_type == 6:
            # Joint powerup - enables short flight but slows player
            image = pg.image.load(
                os.path.join(IMAGEPATH, "powerups/joint.png")
            ).convert_alpha()
        else:
            image = pg.Surface((20, 20))  # Default size for unknown power-ups
            image.fill((255, 255, 0))  # Yellow for unknown power-ups

        # Scale the image to the grid size
        self.image = pg.transform.scale(image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def apply_effect(self, player):
        """Apply power-up effect to player."""
        if self.power_type == 5:
            # Teil powerup - radial blur effect
            player.radial_blur_active = True
        elif self.power_type == 6:
            # Joint powerup: start with pixelation and immediate speed penalty.
            # Flight should enable instantly now. Apply a much stronger
            # pixelation effect for this powerup type, and apply a larger
            # immediate speed penalty.
            player.radial_blur_active = True
            # Store a per-player override for pixelation strength so the
            # global pixelation remains unchanged for other powerups.
            player.joint_pixelation_factor = POWERUP_JOINT_PIXELATION_FACTOR
            # Store original speed so we can restore it exactly on power down
            self._original_speed = player.speed
            player.speed = max(1, player.speed - POWERUP_FLY_SPEED_PENALTY)
            self._applied_fly_penalty = True
            # Enable flying immediately
            player.can_fly = True
        elif self.power_type == 0 or self.power_type == 4:
            # Make the player bigger
            player.image = pg.transform.scale(
                player.image,
                (
                    player.rect.width * POWERUP_SIZE_MULTIPLIER,
                    player.rect.height * POWERUP_SIZE_MULTIPLIER,
                ),
            )
            player.rect = player.image.get_rect(center=player.rect.center)
        elif self.power_type == 1:
            # Make the player faster
            player.speed += POWERUP_SPEED_INCREASE
        elif self.power_type == 2:
            # Change the background
            self.world.change_background()
        elif self.power_type == 3:
            # Chaos effect - 50% chance for one of two effects
            if random.random() < 0.5:
                # Option A: Reverse controls + slow FPS
                player.controls_reversed = True
                self.world.set_fps(POWERUP_CHAOS_FPS)
                self.fps_changed = True
                self.speed_changed = False
            else:
                # Option B: Speed increase
                player.speed += POWERUP_CHAOS_SPEED_INCREASE
                self.speed_changed = True
                self.fps_changed = False

    def power_down(self, player):
        """Remove power-up effect from player."""
        if self.power_type == 5:
            # Remove radial blur effect
            player.radial_blur_active = False
        elif self.power_type == 6:
            # End of joint powerup: ensure flying disabled, remove pixelation and restore speed
            player.can_fly = False
            player.radial_blur_active = False
            # Remove joint-specific pixelation override if present
            if hasattr(player, 'joint_pixelation_factor'):
                delattr(player, 'joint_pixelation_factor')
            if getattr(self, '_applied_fly_penalty', False):
                # Restore the exact original speed we stored on apply
                if hasattr(self, '_original_speed'):
                    player.speed = self._original_speed
                else:
                    # Fallback: add penalty back (shouldn't normally happen)
                    player.speed += POWERUP_FLY_SPEED_PENALTY
                self._applied_fly_penalty = False
        elif self.power_type == 0 or self.power_type == 4:
            # Restore normal size
            player.image = pg.transform.scale(
                player.image,
                (
                    player.rect.width // POWERUP_SIZE_MULTIPLIER,
                    player.rect.height // POWERUP_SIZE_MULTIPLIER,
                ),
            )
            player.rect = player.image.get_rect(center=player.rect.center)
        elif self.power_type == 1:
            # Restore normal speed
            player.speed -= POWERUP_SPEED_INCREASE
        elif self.power_type == 3:
            # Restore effects based on what was activated
            if self.fps_changed:
                player.controls_reversed = False
                self.world.reset_fps()
            if self.speed_changed:
                player.speed -= POWERUP_CHAOS_SPEED_INCREASE

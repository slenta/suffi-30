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
    POWERUP_JOINT_HEAL,
)


class PowerUp(pg.sprite.Sprite):
    """
    PowerUp class for different power-up types in the game.

    Power-up types:
    - Type 0: Makes the player bigger and restores health to full (banana.png)
    - Type 1: Makes the player faster (pulver.png)
    - Type 2: Changes the level background (spraydose.png)
    - Type 3: Chaos effect - reverses left/right controls, increases speed by 6, and has 50% chance to set FPS to 10 for 8 seconds
    - Type 4: Makes the player bigger (babybrei.png)
    - Type 5: Teil - Creates pixelation/rasterization effect for 15 seconds
    - Type 6: Monster - Restores health and makes player faster
            - Type 7: Joint - Halves horizontal movement speed and vertical jump power.
                While active, holding the up key causes the player to continuously ascend
                (press-and-hold to climb). Duration: 10 seconds.

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
        self._original_speed = None

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
            image = pg.image.load(
                os.path.join(IMAGEPATH, "powerups/monster.png")
            ).convert_alpha()
        elif power_type == 7:
            # Joint powerup - enables short flight but slows player
            image = pg.image.load(
                os.path.join(IMAGEPATH, "powerups/joint.png")
            ).convert_alpha()

        # Ensure the sprite has an image and rect so spritecollide works.
        try:
            # Scale powerup image according to POWERUP_SIZE_MULTIPLIER so
            # pickups are visually larger than a single grid cell.
            size_px = int(GRIDSIZE * POWERUP_SIZE_MULTIPLIER)
            self.image = pg.transform.scale(image, (size_px, size_px))
        except Exception:
            # Fallback placeholder image if loading/scaling failed
            size_px = int(GRIDSIZE * POWERUP_SIZE_MULTIPLIER)
            self.image = pg.Surface((size_px, size_px), pg.SRCALPHA)
            self.image.fill((255, 0, 255, 128))

        self.rect = self.image.get_rect()
        # x and y passed in are pixel coordinates (gameworld multiplies by GRIDSIZE)
        try:
            self.rect.center = (x, y)
        except Exception:
            self.rect.topleft = (x, y)

    def apply_effect(self, player):
        """Apply power-up effect to player. Returns duration if type 3, otherwise None."""
        # The power type branches below handle the various effects.
        if self.power_type == 5:
            # Teil powerup - radial blur effect
            player.radial_blur_active = True
        elif self.power_type == 0 or self.power_type == 4:
            # Make the player bigger and restore health to full (type 0)
            if self.power_type == 0:
                player.health = player.max_health
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
            from ..config.constants import POWERUP_CHAOS_DURATION

            if random.random() < 0.5:
                # Option A: Reverse controls + slow FPS (half duration)
                player.controls_reversed = True
                self.world.set_fps(POWERUP_CHAOS_FPS)
                self.fps_changed = True
                self.speed_changed = False
                return POWERUP_CHAOS_DURATION // 2  # 2 seconds
            else:
                # Option B: Speed increase (full duration)
                player.speed += POWERUP_CHAOS_SPEED_INCREASE
                self.speed_changed = True
                self.fps_changed = False
                return POWERUP_CHAOS_DURATION  # 4 seconds
        elif self.power_type == 6:
            # Monster powerup - Restore health and make player faster
            player.health = player.max_health
            player.speed += POWERUP_SPEED_INCREASE
        elif self.power_type == 7:
            # Joint powerup - lower movement tempo and enable slow-fall.
            # Also restore a small amount of health on pickup.
            try:
                heal_amount = int(POWERUP_JOINT_HEAL)
                player.health = min(player.max_health, player.health + heal_amount)
            except Exception:
                pass

            # Reference-counting: store base movement params on the player the
            # first time a joint powerup is applied, and increment a counter
            # so overlapping pickups don't clobber the original values.
            if not hasattr(player, "joint_power_count") or getattr(player, "joint_power_count", 0) <= 0:
                # Save the base values so they can be restored later
                try:
                    setattr(player, "joint_base_speed", getattr(player, "speed", None))
                except Exception:
                    pass
                try:
                    setattr(player, "joint_base_jump_power", getattr(player, "jump_power", None))
                except Exception:
                    pass

            # Increment the active joint counter on the player
            try:
                player.joint_power_count = getattr(player, "joint_power_count", 0) + 1
            except Exception:
                # Defensive fallback
                try:
                    setattr(player, "joint_power_count", 1)
                except Exception:
                    pass

            # Apply the slowed movement relative to the stored base values
            try:
                base_speed = getattr(player, "joint_base_speed", getattr(player, "speed", None))
                base_jump = getattr(player, "joint_base_jump_power", getattr(player, "jump_power", None))
                if base_speed is not None:
                    player.speed = max(0.1, float(base_speed) * 0.5)
                if base_jump is not None:
                    player.jump_power = float(base_jump) * 0.5
            except Exception:
                pass

            # Enable waterfall-like slow fall while the effect is active
            player.slow_fall = True
            self._applied_half_penalty = True
        return None

    def power_down(self, player):
        """Remove power-up effect from player."""
        if self.power_type == 5:
            # Remove radial blur effect
            player.radial_blur_active = False
        elif self.power_type == 7:
            # End of joint powerup: only restore base movement params when
            # there are no more active joint powerups. We decrement a
            # reference counter stored on the player and restore the
            # original values only when it reaches zero.
            try:
                # Decrement counter if present
                count = getattr(player, "joint_power_count", 0)
                if count > 0:
                    player.joint_power_count = count - 1
                else:
                    player.joint_power_count = 0
            except Exception:
                # Defensive: if anything goes wrong, clear joint state
                player.joint_power_count = 0

            # If no more joint powerups active, restore base values
            if getattr(player, "joint_power_count", 0) == 0:
                player.slow_fall = False
                if hasattr(player, "joint_base_speed") and player.joint_base_speed is not None:
                    player.speed = player.joint_base_speed
                    delattr(player, "joint_base_speed")
                if hasattr(player, "joint_base_jump_power") and player.joint_base_jump_power is not None:
                    player.jump_power = player.joint_base_jump_power
                    delattr(player, "joint_base_jump_power")
                # Clean up counter attribute
                try:
                    delattr(player, "joint_power_count")
                except Exception:
                    pass
            # Clear instance flag
            if getattr(self, "_applied_half_penalty", False):
                self._applied_half_penalty = False
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
        elif self.power_type == 1 or self.power_type == 6:
            # Restore normal speed
            player.speed -= POWERUP_SPEED_INCREASE
        elif self.power_type == 3:
            # Restore effects based on what was activated
            if self.fps_changed:
                player.controls_reversed = False
                self.world.reset_fps()
            if self.speed_changed:
                player.speed -= POWERUP_CHAOS_SPEED_INCREASE

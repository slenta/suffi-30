"""Bullet and exploding object projectiles."""

import pygame as pg
import os
import math
from ..config.settings import IMAGEPATH, GRIDSIZE, GRAVITY
from ..config.weapon_config import WEAPON_CONFIG
from ..core.sound_manager import sound_manager
from ..config.constants import (
    EXPLODING_OBJECT_SPEED,
    EXPLODING_OBJECT_INITIAL_VY,
    EXPLODING_OBJECT_GRAVITY_FACTOR,
    EXPLOSION_RANGE,
)


class Bullet(pg.sprite.Sprite):
    """Projectile fired by weapons."""

    def __init__(
        self,
        x,
        y,
        direction_x,
        direction_y,
        weapon_name,
        world,
        from_enemy=False,
        use_gravity=False,
        *groups
    ):
        super().__init__(*groups)
        self.world = world
        self.from_enemy = from_enemy
        self.weapon_name = weapon_name

        # Get weapon stats
        weapon_data = WEAPON_CONFIG.get(weapon_name, WEAPON_CONFIG["gun"])
        self.damage = weapon_data["damage"]
        self.speed = weapon_data.get("bullet_speed", 0)
        self.use_gravity = use_gravity or weapon_data.get("gravity", False)

        # Load bullet image or create colored surface
        bullet_image_path = os.path.join(IMAGEPATH, weapon_data.get("bullet_image", ""))
        try:
            self.image = pg.image.load(bullet_image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, weapon_data["bullet_size"])
        except:
            self.image = pg.Surface(weapon_data["bullet_size"])
            self.image.fill(weapon_data["bullet_color"])

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction_x = direction_x
        self.direction_y = direction_y

        # For gravity-affected bullets we track vertical velocity separately
        if self.use_gravity:
            # horizontal velocity (pixels/frame)
            self.vx = self.direction_x * self.speed
            # initial vertical velocity (pixels/frame)
            self.vy = self.direction_y * self.speed

    def update(self):
        try:
            if self.use_gravity:
                # Gravity-affected projectile: horizontal constant velocity, vertical accelerates
                self.rect.x += int(self.vx)
                self.vy += GRAVITY
                self.rect.y += int(self.vy)
            else:
                self.rect.x += self.direction_x * self.speed
                self.rect.y += self.direction_y * self.speed

            # Check for collisions with platforms
            try:
                if pg.sprite.spritecollideany(self, self.world.platforms):
                    self.kill()
                    return
            except Exception:
                # Defensive: if platforms group is missing or invalid, ignore collision check
                pass

            # Check for collisions
            if self.from_enemy:
                if hasattr(self.world, 'player') and pg.sprite.collide_rect(self, self.world.player):
                    try:
                        self.world.player.take_damage(self.damage)
                    except Exception:
                        pass
                    self.kill()
            else:
                try:
                    hit_enemy = pg.sprite.spritecollideany(self, self.world.enemies)
                except Exception:
                    hit_enemy = None
                if hit_enemy:
                    try:
                        hit_enemy.take_damage(self.damage)
                    except Exception:
                        pass
                    self.kill()
        except Exception as e:
            # Defensive: print and remove bullet if unexpected error occurs during update
            print(f"⚠️ Bullet update error: {e}")
            try:
                self.kill()
            except Exception:
                pass


class ExplodingObject(pg.sprite.Sprite):
    """Throwable explosive object that damages enemies and player in radius."""

    def __init__(self, x, y, direction_x, direction_y, damage, world, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((15, 15))
        self.image.fill((255, 165, 0))  # Orange
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = EXPLODING_OBJECT_SPEED
        self.vy = EXPLODING_OBJECT_INITIAL_VY
        self.damage = damage
        self.world = world
        self.explosion_range = EXPLOSION_RANGE * GRIDSIZE

    def update(self):
        """Update position and check for collision."""
        self.rect.x += self.direction_x * self.speed
        self.vy += GRAVITY * EXPLODING_OBJECT_GRAVITY_FACTOR
        self.rect.y += self.vy

        if pg.sprite.spritecollideany(self, self.world.platforms):
            self.explode()

    def explode(self):
        sound_manager.play_sound_effect("explode")  # Play explosion sound
        # Deal damage to the player
        if pg.sprite.collide_rect(self, self.world.player):
            self.world.player.take_damage(self.damage)

        # Deal damage to all enemies within the explosion range
        for enemy in self.world.enemies:
            distance = math.hypot(
                enemy.rect.centerx - self.rect.centerx,
                enemy.rect.centery - self.rect.centery,
            )
            if distance <= self.explosion_range:
                enemy.take_damage(self.damage)

        # Remove the object after it explodes
        self.kill()


class SprayStream(pg.sprite.Sprite):
    """A continuous spray emitter attached to the player.

    Creates gravity-affected bullets every `fire_rate` frames while active.
    """

    def __init__(self, player, weapon_name, world, *groups):
        super().__init__(*groups)
        self.player = player
        self.weapon_name = weapon_name
        self.world = world
        self.counter = 0
        self.fire_rate = WEAPON_CONFIG.get(weapon_name, {}).get("fire_rate", 2)
        # Provide a minimal image and rect so the sprite can be safely drawn by GameWorld
        # SprayStream itself is invisible; use a 1x1 transparent surface and keep it positioned
        self.image = pg.Surface((1, 1), pg.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()

    def update(self):
        try:
            # Stop emitting if player switched weapons or no longer has it
            if self.player.active_weapon != self.weapon_name or self.weapon_name not in self.player.weapons:
                self.kill()
                return

            self.counter += 1
            if self.counter % max(1, self.fire_rate) != 0:
                return

            # Determine facing direction and emission point
            facing = 1 if getattr(self.player, "vx", 0) >= 0 else -1
            player_rect = getattr(self.player, "rect", pg.Rect(0, 0, 0, 0))
            muzzle_x = player_rect.centerx + int(facing * (player_rect.width // 2 + 2))
            muzzle_y = player_rect.centery

            # Update our own rect so GameWorld.draw() can blit safely
            try:
                self.rect.center = (muzzle_x, muzzle_y)
            except Exception:
                # If rect can't be updated for some reason, keep going (emitter is invisible)
                pass

            # Emit a gravity-affected bullet (droplet)
            b = Bullet(
                muzzle_x,
                muzzle_y,
                facing,
                0,
                self.weapon_name,
                self.world,
                from_enemy=False,
                use_gravity=True,
            )
            # Safely add to groups
            try:
                self.world.bullets.add(b)
                self.world.all_sprites.add(b)
            except Exception:
                # If groups are in an inconsistent state, ensure bullet still exists
                pass
        except Exception as e:
            # Defensive: if anything goes wrong during emission, remove the emitter to avoid crashing the game loop
            print(f"⚠️ SprayStream error: {e}")
            try:
                self.kill()
            except Exception:
                pass

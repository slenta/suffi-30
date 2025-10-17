import pygame as pg
import os
from .settings import *
from .weapon_stats import WEAPON_CONFIG
from .sound_manager import sound_manager  # Import the sound manager
import math


class Bullet(pg.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        direction_x,
        direction_y,
        weapon_name,
        world,
        from_enemy=False,
        *groups
    ):
        super().__init__(*groups)
        self.world = world
        self.from_enemy = from_enemy
        self.weapon_name = weapon_name

        # Get weapon stats
        weapon_data = WEAPON_CONFIG.get(weapon_name, WEAPON_CONFIG["gun"])
        self.damage = weapon_data["damage"]
        self.speed = weapon_data["bullet_speed"]

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

    def update(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Check for collisions with platforms
        if pg.sprite.spritecollideany(self, self.world.platforms):
            self.kill()

        # Check for collisions
        if self.from_enemy:
            if pg.sprite.collide_rect(self, self.world.player):
                self.world.player.take_damage(self.damage)
                self.kill()
        else:
            hit_enemy = pg.sprite.spritecollideany(self, self.world.enemies)
            if hit_enemy:
                hit_enemy.take_damage(self.damage)
                self.kill()


class ExplodingObject(pg.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, damage, world, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((15, 15))  # Size of the exploding object
        self.image.fill((255, 165, 0))  # Orange color for the object
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = 3  # Slower speed for the exploding object
        self.vy = -3  # Vertical velocity
        self.damage = damage
        self.world = world
        self.explosion_range = 3 * GRIDSIZE  # Explosion range in pixels (3 tiles)

    def update(self):
        # Apply horizontal movement
        self.rect.x += self.direction_x * self.speed

        # Apply gravity
        self.vy += GRAVITY * 0.2
        self.rect.y += self.vy

        # Check for collisions with platforms (blocks)
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

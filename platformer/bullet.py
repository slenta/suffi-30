import pygame as pg
from .settings import *
import math


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, damage, world, from_enemy=False):
        super().__init__()
        self.image = pg.Surface((20, 9))  # Bullet size
        self.image.fill(
            (255, 0, 0) if from_enemy else (0, 255, 0)
        )  # Red for enemy bullets, green for player bullets
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction_x = direction_x  # X direction of the bullet
        self.direction_y = direction_y  # Y direction of the bullet
        self.speed = BULLET_SPEED
        self.damage = damage  # Damage dealt by the bullet
        self.world = world
        self.from_enemy = from_enemy  # Flag to indicate if the bullet is from an enemy

    def update(self):
        # Move the bullet
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Remove the bullet if it goes off-screen
        if (
            self.rect.right < self.world.ground_start
            or self.rect.left > self.world.ground_end
        ):
            self.kill()

        # Check for collisions with platforms (blocks)
        if pg.sprite.spritecollideany(self, self.world.platforms):
            self.kill()

        # Check for collisions
        if self.from_enemy:
            # Enemy bullets can hit the player
            if pg.sprite.collide_rect(self, self.world.player):
                self.world.player.take_damage(self.damage)
                self.kill()
        else:
            # Player bullets can hit enemies
            hit_enemy = pg.sprite.spritecollideany(self, self.world.enemies)
            if hit_enemy:
                hit_enemy.take_damage(self.damage)
                self.kill()


class ExplodingObject(pg.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, damage, world):
        super().__init__()
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

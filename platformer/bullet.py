import pygame as pg
from .settings import *


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, world):
        super().__init__()
        self.image = pg.Surface((10, 5))  # Bullet size
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.world = world
        self.speed = (
            BULLET_SPEED * self.world.direction
        )  # Bullet speed based on direction

    def update(self):
        self.rect.x += self.speed
        # Remove the bullet if it goes off-screen
        if (
            self.rect.right < self.world.ground_start
            or self.rect.left > self.world.ground_end
        ):
            self.kill()

        # Check for collisions with obstacles/items/blocks
        if pg.sprite.spritecollideany(self, self.world.platforms):
            self.kill()

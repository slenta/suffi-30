import pygame as pg
import os
from .settings import *


## Class Player
class Player(pg.sprite.Sprite):

    def __init__(self, _x, _y, world, start_gems=0):
        super().__init__()
        self.img = []
        for i in range(2):
            player_image = pg.image.load(
                os.path.join(IMAGEPATH, "alien_green_0" + str(i) + ".png")
            ).convert_alpha()
            self.img.append(player_image)
        self.image = self.img[0]
        self.rect = self.image.get_rect()
        self.rect.x = _x * GRIDSIZE
        self.rect.bottom = _y * GRIDSIZE
        # self.rect.topleft = (self.rect.x, self.rect.y)
        self.speed = PLAYER_SPEED
        self.jump_power = JUMP_POWER
        self.vx = 0
        self.vy = 0
        self.gems = start_gems
        self.world = world

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        self.rect.y -= 2
        if len(hits) > 0:
            self.vy = -1 * self.jump_power

    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy > MAX_VELOCITY:
            self.vy = MAX_VELOCITY

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:  # LEFT
            self.vx = -1 * self.speed
        elif keys[pg.K_d]:  # RIGHT
            self.vx = self.speed
        elif keys[pg.K_w]:  # JUMP
            self.jump()
        else:
            self.vx = 0

        # Horizonfale Kollision
        self.rect.x += self.vx
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right

        # Vertikale Kollision
        self.rect.y += self.vy
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom
            self.vy = 0

        # Von der Plattform runterfallen
        if self.rect.y > self.world.top + 20:
            print(self.rect)
            self.loose()

    def check_edges(self):
        left_edge = self.world.ground_start
        right_edge = self.world.ground_end
        if self.rect.left < left_edge:
            self.rect.left = left_edge
        elif self.rect.right > right_edge:
            self.rect.right = right_edge

    def check_items(self):
        hits = pg.sprite.spritecollide(self, self.world.items, True)
        for item in hits:
            item.apply(self)
            print(self.gems)  # Nur für Testzwecke

    def loose(self):
        if self.gems >= 1:
            self.gems -= 1
            self.world.loose_screen()
            self.world.reset()
        else:
            self.world.game_over()

    def update(self):
        self.apply_gravity()
        self.check_edges()
        self.move()
        self.check_items()


## End Class Player

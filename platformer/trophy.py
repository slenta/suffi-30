import pygame as pg
import os
from .settings import IMAGEPATH, GRIDSIZE


class Trophy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = pg.image.load(os.path.join(IMAGEPATH, "trophy.png")).convert_alpha()
        self.image = pg.transform.scale(image, (GRIDSIZE, GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.closed_image = pg.image.load(
            os.path.join(IMAGEPATH, "door_closed.png")
        ).convert_alpha()
        self.open_image = pg.image.load(
            os.path.join(IMAGEPATH, "door_open.png")
        ).convert_alpha()
        self.image = pg.transform.scale(self.closed_image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_open = False

    def open(self):
        self.image = pg.transform.scale(self.open_image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.is_open = True

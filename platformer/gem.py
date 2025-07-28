import pygame as pg
from .settings import *


class Gem(pg.sprite.Sprite):

    def __init__(self, _x, _y, _image):
        super().__init__()
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.x = _x * GRIDSIZE
        self.rect.y = _y * GRIDSIZE

    def apply(self, character):
        character.gems += 1


## End Class Gem

import pygame as pg
import os
from .settings import IMAGEPATH, GRIDSIZE
from .weapon_stats import WEAPON_CONFIG


class WeaponPickup(pg.sprite.Sprite):
    def __init__(self, x, y, weapon_name):
        super().__init__()
        self.weapon_name = weapon_name

        if weapon_name not in WEAPON_CONFIG:
            raise ValueError(f"Unknown weapon: {weapon_name}")

        weapon_data = WEAPON_CONFIG[weapon_name]
        image_path = os.path.join(IMAGEPATH, weapon_data["image"])

        self.image = pg.transform.scale(
            pg.image.load(image_path).convert_alpha(), (GRIDSIZE, GRIDSIZE)
        )
        print(f"Loaded weapon image for {weapon_name} from {image_path}")

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

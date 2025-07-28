# Einfacher Platformer, Version 0.2
# Nach einer Idee von Jonathan Cooper
# (https://www.youtube.com/playlist?list=PLk64HPu_u_NOD0hC2XFZfDu1ZOr7OF1qB)
# Sprites und Tiles: Pixel Platformer (CC0) von Kenney.nl
# (https://www.kenney.nl/assets/pixel-platformer)
# Jörg Kantel, 2023
import pygame as pg
import asyncio
from pygame.locals import *
import os, sys

## Settings
GRIDSIZE = 18
GRID_WIDTH = 40
GRID_HEIGHT = 15
WIDTH, HEIGHT = GRID_WIDTH * GRIDSIZE, GRID_HEIGHT * GRIDSIZE
TITLE = "Simple Platformer"
FPS = 60  # Frames per second
PLAYER_WIDTH = 24
PLAYER_HEIGHT = 24
PLAYER_START_X, PLAYER_START_Y = 5, 1
PLAYER_SPEED = 3

# Physikalische Konstanten
GRAVITY = 0.5
MAX_VELOCITY = 18
JUMP_POWER = 10

## Hier wird der Pfad zum Verzeichnis der Assets gesetzt
IMAGEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/images")

## Farben
BG_COLOR = (65, 166, 246)  # Himmelblau


## Class GameWorld
class GameWorld:

    def __init__(self):
        # Pygame und das Fenster initialisieren
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.keep_going = True

    def reset(self):
        # Neustart oder Status zurücksetzen
        # Hier werden alle Elemente der GameWorld initialisiert
        ## Load Assets
        grass_image = pg.image.load(
            os.path.join(IMAGEPATH, "grass_02.png")
        ).convert_alpha()
        block_image = pg.image.load(
            os.path.join(IMAGEPATH, "block_00.png")
        ).convert_alpha()
        gem_image = pg.image.load(os.path.join(IMAGEPATH, "gem.png")).convert_alpha()
        grass_locations = []
        for i in range(GRID_WIDTH):
            grass_loc = (i, GRID_HEIGHT - 1)
            grass_locations.append(grass_loc)
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        for loc in grass_locations:
            x = loc[0]
            y = loc[1]
            p = Platform(x, y, grass_image)
            self.platforms.add(p)
            self.all_sprites.add(p)

        block_locations = [
            (18, 4),
            (19, 4),
            (20, 4),
            (21, 4),
            (11, 7),
            (12, 7),
            (13, 7),
            (14, 7),
            (25, 7),
            (26, 7),
            (27, 7),
            (17, 10),
            (18, 10),
            (19, 10),
            (38, 12),
            (38, 13),
        ]
        for loc in block_locations:
            x = loc[0]
            y = loc[1]
            p = Platform(x, y, block_image)
            self.platforms.add(p)
            self.all_sprites.add(p)

        gem_locations = [(20, 3), (12, 6), (26, 6), (36, 13)]
        self.items = pg.sprite.Group()
        for loc in gem_locations:
            x = loc[0]
            y = loc[1]
            g = Gem(x, y, gem_image)
            self.items.add(g)
            self.all_sprites.add(g)

        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        self.player_sprite_group = pg.sprite.GroupSingle()
        self.player_sprite_group.add(self.player)
        self.all_sprites.add(self.player)

    def events(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.keep_going = False
                self.game_over()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def start_screen(self):
        pass

    def win_screen(self):
        pass

    def loose_screen(self):
        pass

    def game_over(self):
        # print("Bye, Bye, Baby!")
        pg.quit()
        sys.exit()


## Ende Class GameWorld


## Class Platform
class Platform(pg.sprite.Sprite):

    def __init__(self, _x, _y, _image):
        super().__init__()
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.x = _x * GRIDSIZE
        self.rect.y = _y * GRIDSIZE


## End Class Platform


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


## Class Player
class Player(pg.sprite.Sprite):

    def __init__(self, _x, _y):
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
        self.gems = 0

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, world.platforms, False)
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
            if self.rect.x > 0:
                self.vx = -1 * self.speed
        elif keys[pg.K_d]:  # RIGHT
            if self.rect.x < WIDTH - PLAYER_WIDTH:
                self.vx = self.speed
        elif keys[pg.K_w]:  # JUMP
            self.jump()
        else:
            self.vx = 0
        # Horizonfale Kollision
        self.rect.x += self.vx
        hits = pg.sprite.spritecollide(self, world.platforms, False)
        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right
        # Vertikale Kollision
        self.rect.y += self.vy
        hits = pg.sprite.spritecollide(self, world.platforms, False)
        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom
            self.vy = 0

    def check_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def check_items(self):
        hits = pg.sprite.spritecollide(self, world.items, True)
        for item in hits:
            item.apply(self)
            print(self.gems)  # Nur für Testzwecke

    def update(self):
        self.apply_gravity()
        self.move()
        self.check_edges()
        self.check_items()


## End Class Player

# Hauptprgramm
world = GameWorld()
world.start_screen()
world.reset()


# Hauptschleife
async def main():
    while world.keep_going:
        world.clock.tick(FPS)
        world.events()
        world.update()
        world.draw()
        await asyncio.sleep(0)  # Very important, and keep it 0


asyncio.run(main())

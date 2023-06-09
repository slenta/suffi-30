# Einfacher Platformer, Version 0.1
# Sprites und Tiles: Pixel Platformer (CC0) von Kenney.nl
# https://www.kenney.nl/assets/pixel-platformer
# Jörg Kantel, 2023
import pygame as pg
import asyncio
from pygame.locals import *
import os, sys

## Settings
GRIDSIZE = 18
GRID_WIDTH = 40
GRID_HEIGHT = 15
WIDTH, HEIGHT = GRID_WIDTH*GRIDSIZE, GRID_HEIGHT*GRIDSIZE
TITLE = "Simple Platformer"
FPS = 60                     # Frames per second
PLAYER_WIDTH = 24
PLAYER_HEIGHT = 24
PLAYER_SPEED = 5

## Hier wird der Pfad zum Verzeichnis der Assets gesetzt
DATAPATH = os.path.join(os.getcwd(), "data")

## Farben
BG_COLOR = (65, 166, 246)     # Himmelblau

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
        grass_image = pg.image.load(os.path.join(DATAPATH, "grass_02.png")).convert_alpha()
        # block_image = pg.image.load(os.path.join(DATAPATH, "block_00.png")).convert_alpha()

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

        self.player = Player(PLAYER_WIDTH, HEIGHT - PLAYER_HEIGHT-GRIDSIZE)
        self.all_sprites.add(self.player)
  
    def events(self):
        for event in pg.event.get():
            if ((event.type == pg.QUIT)
                or (event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE)):
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
        self.rect.x = _x*GRIDSIZE
        self.rect.y = _y*GRIDSIZE
## End Class Platform

## Class Player
class Player(pg.sprite.Sprite):

    def __init__(self, _x, _y):
        super().__init__()
        self.img = []
        for i in range(2):
            player_image = pg.image.load(os.path.join(DATAPATH, "alien_green_0" + str(i) + ".png")).convert_alpha()
            self.img.append(player_image)
        self.image = self.img[0]
        self.rect = self.image.get_rect()
        self.x = _x
        self.y = _y
        self.rect.topleft = (self.x, self.y)
        self.dx = PLAYER_SPEED

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:        # LEFT
            if self.x > 0:
                self.x -= self.dx
        elif keys[pg.K_d]:      # RIGHT
            if self.x < WIDTH - PLAYER_WIDTH:
                self.x += self.dx
        else:
            self.x += 0
            self.y += 0
        self.rect.topleft = (self.x, self.y)
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
# A night in a secret garden
# Kenney Game Jam 2023
# Jörg Kantel
import pygame as pg
import asyncio
from pygame.locals import *
import os, sys

## Settings
GRIDSIZE = 16
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH, HEIGHT = GRID_WIDTH*GRIDSIZE, GRID_HEIGHT*GRIDSIZE
TITLE = "A Night in a Secret Garden"
FPS = 60           # Frames per second
PLAYER_START_X, PLAYER_START_Y = 28, 20

## Hier wird der Pfad zum Verzeichnis der Assets gesetzt
IMAGEPATH = os.path.join(os.getcwd(), "data/images")

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
        pass
        ## Load Assets

    def events(self):
        for event in pg.event.get():
            if ((event.type == pg.QUIT)
                or (event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE)):
                self.keep_going = False
                self.game_over()

    def update(self):
        pass

    def draw(self):
        pg.display.flip()

    def game_over(self):
        # print("Bye, Bye, Baby!")
        pg.quit()
        sys.exit()
## Ende Class GameWorld

# Hauptprogramm
world = GameWorld()
world.reset()

# Hauptschleife
async def main():
    while world.keep_going:
        world.clock.tick(FPS)
        world.events()
        world.update()
        world.draw()
        await asyncio.sleep(0)     # Very important, and keep it 0

asyncio.run(main())
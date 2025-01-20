# Pygbag Boilerplate
import asyncio
import pygame as pg
from pygame.locals import *
import os, sys

## Settings
WIDTH, HEIGHT =  800, 450
TITLE = "Pygbag Boilerplate"
FPS = 60                   # Frames per second

## Hier wird der Pfad zum Verzeichnis der Assets gesetzt
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

## Farben
BG_COLOR = (40, 40, 40)  # Dunkelgrau

# Klassen

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
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
    
    def run(self):
        # Game Loop
        pass
  
    def events(self):
        for event in pg.event.get():
            if ((event.type == pg.QUIT)
                or (event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE)):
                if self.playing:
                    self.playing = False
                self.keep_going = False
 
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def start_screen(self):
        pass
    
    def game_over_screen(self):
        # print("Game Over")
        pass    
## Ende Class GameWorld
    

## Class Player
class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # Load Image
        img = pg.image.load(os.path.join(DATAPATH, "pygbag_logo.png")).convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()
        self.x, self.y = WIDTH/2, HEIGHT/2
        self.rect.center = (self.x, self.y)
    
    def update(self):
        pass
## End Class Player


# --------------------------- Hauptprgramm --------------------------- #
world = GameWorld()
world.start_screen()

# Hauptschleife
async def main():
    while world.keep_going:
        world.reset()
        world.playing = True
        while world.playing:
            world.clock.tick(FPS)
            world.events()
            world.update()
            world.draw()
            await asyncio.sleep(0)  # Very important, and keep it 0
        world.game_over_screen()
    pg.quit()
    sys.exit()

asyncio.run(main())


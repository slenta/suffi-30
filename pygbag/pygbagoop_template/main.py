# Pygame OOP-Template zur Verwendung mit Pygbag Version 0.2
import asyncio
import pygame as pg
from pygame.locals import *
import os, sys

## Settings
WIDTH, HEIGHT =  800, 450  #  640, 480 – 16x16: 40, 30; 32x32: 20, 15
TITLE = "Pygame (Pygbag) OOP Template v02"
FPS = 60                   # Frame per second
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 45
PLAYER_SPEED = 5

## Hier wird der Pfad zum Verzeichnis der Assets gesetzt
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

## Farben
BG_COLOR = (40, 40, 40)

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
        # self.run()
    
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
        img = pg.image.load(os.path.join(DATAPATH, "platformchar_idle.png")).convert_alpha()
        # img = pg.image.load("data/platformchar_idle.png").convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()
        self.x, self.y = WIDTH/2, HEIGHT/2
        self.speed = PLAYER_SPEED
    
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:     # UP
            if self.y > PLAYER_HEIGHT - 20:
                self.y -= self.speed
        elif keys[pg.K_s] or keys[pg.K_DOWN]:   # DOWN
            if self.y < HEIGHT - PLAYER_HEIGHT:
                self.y += self.speed
        elif keys[pg.K_a] or keys[pg.K_LEFT]:   # LEFT
            if self.x > PLAYER_WIDTH:
                self.x -= self.speed
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:   # RIGHT
            if self.x < WIDTH - PLAYER_WIDTH:
                self.x += self.speed
        else:
            self.x += 0
            self.y += 0
        self.rect.center = (self.x, self.y)
## End Class Player

# Hauptprgramm
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

# Bouncing Faces
import asyncio
import pygame as pg
from pygame.locals import *
import os, sys
from random import randint

## Settings
WIDTH, HEIGHT =  800, 450
TITLE = "Bouncing Faces"
FPS = 60                   # Frames per second
N_FACES = 50               # Number of Faces

## Hier wird der Pfad zum Verzeichnis der Assets gesetzt
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
## Array mit den Bildern
face_images = ["face01.png", "face02.png", "face03.png", "face04.png",
               "face05.png", "face06.png", "face07.png", "face08.png",
               "face09.png", "face10.png", "face11.png", "face12.png"]

## Farben
BG_COLOR = ("#2b3e50")

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
        self.faces = []
        for i in range(N_FACES):
            face = Face(face_images[randint(0, len(face_images) - 1)])
            self.faces.append(face)
            self.all_sprites.add(face)
    
    def events(self):
        for event in pg.event.get():
            if ((event.type == pg.QUIT)
                or (event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE)):
                if self.playing:
                    self.playing = False
                self.keep_going = False
 
    def update(self):
        # self.face.check_edges()
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
    

## Class Face
class Face(pg.sprite.Sprite):

    def __init__(self, img):
        pg.sprite.Sprite.__init__(self)
        # Load Image
        img = pg.image.load(os.path.join(DATAPATH, img)).convert_alpha()
        self.r = randint(12, 24)
        self.image = pg.transform.scale(img, (self.r*2, self.r*2))
        self.rect = self.image.get_rect()
        self.x = randint(self.r, WIDTH - self.r);
        self.y = randint(self.r, HEIGHT - self.r);
        self.rect.center = (self.x, self.y)
        self.loc = pg.math.Vector2(self.x, self.y)
        self.vel = pg.math.Vector2(randint(-3, 3), randint(-3, 3))
        if self.vel.x == 0:
            self.vel.x = 1
        if self.vel.y == 0:
            self.vel.y = -1
    
    def update(self):
        self.check_edges()
        self.loc += self.vel
        self.x = self.loc.x
        self.y = self.loc.y
        self.rect.center = (self.x, self.y)
        
    def check_edges(self):
        if (self.loc.y >= HEIGHT - self.r):
            self.vel.y *= -1
            self.loc.y = (HEIGHT - self.r)
        elif (self.loc.y <= self.r):
            self.vel.y *= -1
            self.loc.y = self.r
            
        if (self.loc.x >= WIDTH - self.r):
            self.vel.x *= -1
            self.loc.x = (WIDTH - self.r)
        elif (self.loc.x <= self.r):
            self.vel.x *= -1
            self.loc.x = self.r
## End Class Face


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



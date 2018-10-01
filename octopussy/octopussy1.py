import pygame as pg
from pygame.locals import *  # Wenn dies nicht importiert wird,
                             # kann man UTF-8 (Umlaute) knicken
import os
import random as r

### Klassendefinitionen --------------------------------------------------


class SpaceShip(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.posx = r.randint(1024, 2048)
        self.posy = r.randint(20, 460)
    
    def update(self):
        self.rect.centerx += self.dx
        if self.rect.left > win.get_width():
            self.rect.right = 0
            self.rect.centery = r.randrange(50, win.get_height()-85)
        elif self.rect.right < 0:
            self.rect.left = win.get_width()
            self.rect.centery = r.randrange(50, win.get_height()-85)

class RocketBoy(SpaceShip):
    
    def __init__(self):
        SpaceShip.__init__(self)
        self.image = pg.image.load("images/rocketboy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.dx = r.randint(-6, -3)
   

class Planet(SpaceShip):
    
    def __init__(self):
        SpaceShip.__init__(self)
        self.image = pg.image.load("images/planet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.dx = r.randint(-2, -1)
   

class Octopussy(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.posx = 80
        self.posy = 240
        self.image = pg.image.load("images/octopussy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.dy = 0
                

    def update(self):
        self.rect.centery += self.dy
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= win.get_height():
            self.rect.bottom = win.get_height()


## Ende Klassendefinitionen ----------------------------------------------

pg.init()


win = pg.display.set_mode((1024, 640))
pg.display.set_caption("Octopussy – On the Way Home")

background = pg.Surface(win.get_size())
background = background.convert()
background.fill((0, 80, 125))

# Hier wird der Pfad zum Verzeichnis des ».py«-Files gesetzt
# Erspart einem das Herumgehample in TextMate mit dem os.getcwd()
# und os.path.join()
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

# Assets laden
# background = pg.image.load("images/background.png").convert()
win.blit(background, (0, 0))


# Klassen laden
octopussy = Octopussy()
rocketboys = []
for i in range(3):
    rocketboy = RocketBoy()
    rocketboys.append(rocketboy)
planets = []
for i in range(2):
    planet = Planet()
    planets.append(planet)
allSprites = pg.sprite.Group(planets, rocketboys, octopussy)

clock = pg.time.Clock()
clock.tick(30)  # Framerate

keep_going = True
while keep_going:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            keep_going = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                keep_going = False
            elif event.key == pg.K_UP:
                octopussy.dy = -4
            elif event.key == pg.K_DOWN:
                octopussy.dy = 4
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                octopussy.dy = 0

    allSprites.clear(win, background)
    allSprites.update()
    allSprites.draw(win)
    
    pg.display.flip()
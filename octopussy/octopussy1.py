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
            self.reset()
        elif self.rect.right < 0:
            self.rect.left = win.get_width()
            self.reset()
    
    def reset(self):
        self.rect.centerx = r.randint(1040, 2080)
        self.rect.centery = r.randint(20, 460)
        self.dx = r.randint(self.max_speed, self.min_speed)

class RocketBoy(SpaceShip):
    
    def __init__(self):
        SpaceShip.__init__(self)
        self.image = pg.image.load("images/rocketboy.png").convert_alpha()
        self.rect = self.image.get_rect()
        # self.rect.inflate(0, -10)
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.max_speed = -6
        self.min_speed = -3
        self.dx = r.randint(self.max_speed, self.min_speed)
   

class Planet(SpaceShip):
    
    def __init__(self):
        SpaceShip.__init__(self)
        self.image = pg.image.load("images/planet.png").convert_alpha()
        self.rect = self.image.get_rect()
        # self.rect.inflate_ip(-60, -60)
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.max_speed = -2
        self.min_speed = -1
        self.dx = r.randint(self.max_speed, self.min_speed)
   

class Octopussy(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.posx = 80
        self.posy = 240
        self.image = pg.image.load("images/octopussy.png").convert_alpha()
        self.rect = self.image.get_rect()
        # self.rect.inflate(-15, -25)
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

hearts = 10
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
    
    # Kollisionserkennung
    for rocketboy in rocketboys:
        if rocketboy.rect.colliderect(octopussy.rect):
            hearts -= 1
            print("Kollision! Hearts = ", hearts)
            if hearts <= 0:
                keep_going = False
            rocketboy.reset()

    for planet in planets:
        if planet.rect.colliderect(octopussy.rect):
            if hearts < 10:
                hearts += 1
            print("Auftanken! Hearts = ", hearts)
            planet.reset()

    allSprites.clear(win, background)
    allSprites.update()
    allSprites.draw(win)
    
    pg.display.flip()
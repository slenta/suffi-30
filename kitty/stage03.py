# Space Cute

import pygame as pg
from pygame.locals import *  # Wenn dies nicht importiert wird,
                             # kann man UTF-8 (Umlaute) knicken
import os, sys
import random

FPS = 1                     # Framerate

pg.init()

class Spaceship(pg.sprite.Sprite):
    
    def __init__(self, pic, posx, posy):
        pg.sprite.Sprite.__init__(self)
        self.pic = pic
        self.posx = posx
        self.posy = posy
        self.image = pg.image.load(self.pic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.dx = 0
        self.dy = 0
        
    def update(self):
        self.rect.centerx += self.dx
        if self.rect.left > win.get_width():
            self.rect.right = 0
            self.rect.centery = random.randrange(50, win.get_height()-85)
        elif self.rect.right < 0:
            self.rect.left = win.get_width()
            self.rect.centery = random.randrange(50, win.get_height()-85)


win = pg.display.set_mode((800, 600))
pg.display.set_caption("Space Cute")

# Hier wird der Pfad zum Verzeichnis des ».py«-Files gesetzt
# Erspart einem das Herumgehample in TextMate mit dem os.getcwd()
# und os.path.join()
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

# Assets laden
background = pg.image.load("images/background.png").convert()
win.blit(background, (0, 0))

planet    = Spaceship("images/planet.png", 500, 500)
planet.dx = 1
rocket    = Spaceship("images/rocketship.png", 300, 300)
rocket.dx = 10
octopussy = Spaceship("images/octopus2.png", 400, 400)
octopussy.dx = -5
beetle    = Spaceship("images/beetleship.png", 200, 200)
beetle.dx = 3
allSprites = pg.sprite.Group(planet, rocket, octopussy, beetle)

clock = pg.time.Clock()
clock.tick(FPS)  # Framerate

keep_going = True
while keep_going:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            keep_going = False
    
    allSprites.clear(win, background)
    allSprites.update()
    allSprites.draw(win)
    
    pg.display.flip()

sys.exit()
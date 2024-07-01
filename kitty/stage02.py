# Walking Kitty

import pygame as pg
from pygame.locals import *  # Wenn dies nicht importiert wird,
                             # kann man UTF-8 (Umlaute) knicken
import os, sys
import random
pg.init()

win = pg.display.set_mode((640, 480))
pg.display.set_caption("Lauf, Hörnchen, Lauf!")

# Assets laden
# Hier wird der Pfad zum Verzeichnis des ».py«-Files gesetzt
# Erspart einem das Herumgehample in TextMate mit dem os.getcwd()
# und os.path.join()
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

class Kitty(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/horngirl.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 275
        self.rect.centery = 240
        self.dx = 0.05
        self.dy = 0
        
    def update(self):
        self.rect.centerx += self.dx
        if self.rect.left > win.get_width():
            self.rect.right = 0
            self.rect.centery = random.randrange(50, win.get_height()-85)

background = pg.Surface(win.get_size())
background = background.convert()
background.fill((0, 80, 125))
win.blit(background, (0, 0))

kitty = Kitty()
allSprites = pg.sprite.Group(kitty)

clock = pg.time.Clock()
clock.tick(30)  # Framerate

keep_going = True
while keep_going:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            keep_going = False
            pg.quit()  # ????
            sys.exit()
    
    allSprites.clear(win, background)
    allSprites.update()
    allSprites.draw(win)
    
    pg.display.flip()
            
# coding=utf-8

# Minimales PyGame-Grundgerüst
# Als Template für alle Python/PyGame-Projekte verwenden

import pygame as pg
from pygame.locals import *  # Wenn dies nicht importiert wird,
                             # kann man UTF-8 (Umlaute) knicken
pg.init()

win = pg.display.set_mode((640, 480))
pg.display.set_caption("Hallo Wörld!")

background = pg.Surface(win.get_size())
background = background.convert()
background.fill((0, 80, 125))

clock = pg.time.Clock()
clock.tick(30)  # Framerate

keep_going = True
while keep_going:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            keep_going = False

    win.blit(background, (0, 0))
    pg.display.flip()
            
# Hello Kitty

import pygame as pg
from pygame.locals import *  # Wenn dies nicht importiert wird,
                             # kann man UTF-8 (Umlaute) knicken
import os
pg.init()

win = pg.display.set_mode((640, 480))
pg.display.set_caption("Hallo Hörnchen")

background = pg.Surface(win.get_size())
background = background.convert()
background.fill((0, 80, 125))

# Assets laden
# Hier wird der Pfad zum Verzeichnis des ».py«-Files gesetzt
# Erspart einem das Herumgehample in TextMate mit dem os.getcwd()
# und os.path.join()
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

horngirl = pg.image.load("images/horngirl.png").convert_alpha()

# Text
textfont = pg.font.SysFont("", 64)
myMessage  = "Hallo Kitty!"

clock = pg.time.Clock()
clock.tick(30)  # Framerate

keep_going = True
while keep_going:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            keep_going = False

    win.blit(background, (0, 0))
    win.blit(horngirl, (275, 100))
    myText = textfont.render(myMessage, True, (255, 255, 255))
    win.blit(myText, (200, 280))
    
    pg.display.flip()
            
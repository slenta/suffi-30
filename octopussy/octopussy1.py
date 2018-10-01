import pygame as pg
from pygame.locals import *  # Wenn dies nicht importiert wird,
                             # kann man UTF-8 (Umlaute) knicken
import os

### Klassendefinitionen --------------------------------------------------

class Octopussy(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.posx = 80
        self.posy = 240
        self.image = pg.image.load("images/octopussy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.gravity = 0.6
        self.lift = -24
        self.velocity = 0
                
    def up(self):
        self.velocity += self.lift
            
    def update(self):
        self.velocity += self.gravity
        self.velocity *= 0.9
        self.rect.centery += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= win.get_height():
            self.rect.bottom = win.get_height()

class Space(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        self.image = pg.image.load("images/background.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.dx = 20
        self.rect.left = 0
    
    def update(self):
        self.rect.left -= self.dx
        if self.rect.left >= 0:
            self.reset()
    
    def reset(self):
        self.rect.left = 0

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
# space = Space()
allSprites = pg.sprite.Group(octopussy)

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
            elif event.key == pg.K_SPACE:
                octopussy.velocity += octopussy.lift
        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                octopussy.velocity = 0

    allSprites.clear(win, background)
    allSprites.update()
    allSprites.draw(win)
    
    pg.display.flip()
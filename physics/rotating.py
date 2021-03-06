# Rotierendes Raumschiff

import pygame
from pygame.locals import *
import os

# Hier wird der Pfad zum Verzeichnis des ».py«-Files gesetzt
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

# Konstanten deklarieren
WIDTH, HEIGHT = 500, 500
TITLE = "Rotating Space Ship"
FPS = 60
# BG = (234, 218, 184) # Packpapier-Farbe
BG = (49, 197, 244) # Coding Train Blue

# Pygame initialisieren und das Fenster und die Hintergrundfarbe festlegen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

class Ship(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.imageMaster = pygame.image.load("ship.png").convert()
        self.imageMaster = pygame.transform.scale(self.imageMaster, (24, 30))
        
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.dir = 0
        self.speed = 0
        self.dx = 0
        self.dy = 0
        
    def update(self):
        
    

def update():
    pass

def draw():
    pass

keep_going = True
while keep_going:
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT)
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            keep_going = False

    screen.fill(BG)
    update()
    draw()
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
import pygame
from pygame.locals import *
import os

# Hier wird der Pfad zum Verzeichnis des ».py«-Files gesetzt
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

# Konstanten deklarieren
WIDTH, HEIGHT = 500, 500
TITLE = "🐍 Pygame Boilerplate 🐍"
FPS = 60
# BG = (234, 218, 184) # Packpapier-Farbe
BG = (49, 197, 244) # Coding Train Blue

# Pygame initialisieren und das Fenster und die Hintergrundfarbe festlegen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

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
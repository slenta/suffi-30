# In ach Richtungen rotierendes Raumschiff

import pygame
from pygame.locals import *
import os

# Hier wird der Pfad zum Verzeichnis des ».py«-Files gesetzt
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

# Konstanten deklarieren
WIDTH, HEIGHT = 640, 480
TITLE = "Rotating Space Ship in 8 Directions"
FPS = 60
# BG = (234, 218, 184) # Packpapier-Farbe
BG = (49, 197, 244)  # Coding Train Blue
# BG = (0, 80, 125)      # Dunkelblau

class Ship(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.imageMaster = pygame.image.load("images/ship.png").convert()
        self.imageMaster = pygame.transform.scale(self.imageMaster, (48, 60))
        
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
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
        
        self.calcVector()
        self.x += self.dx
        self.y += self.dy
        self.checkBounds()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
    def turnLeft(self):
        self.dir += 45
        if self.dir >= 360:
            self.dir = 45
    
    def turnRight(self):
        self.dir -= 45
        if self.dir <= 0:
            self.dir = 315
    
    def speedUp(self):
        self.speed += 1
        if self.speed > 8:
            self.speed = 8
    
    def slowDown(self):
        self.speed -= 1
        if self.speed < 0:
            self.speed = 0
        
    def calcVector(self):
        if self.dir == 0:
            self.dx = 1
            self.dy = 0
        elif self.dir == 45:
            self.dx = 0.7
            self.dy = -0.7
        elif self.dir == 90:
            self.dx = 0
            self.dy = -1
        elif self.dir == 135:
            self.dx = -0.7
            self.dy = -0.7
        elif self.dir == 180:
            self.dx = -1
            self.dy = 0
        elif self.dir == 225:
            self.dx = -0.7
            self.dy = 0.7
        elif self.dir == 270:
            self.dx = 0
            self.dy = 1
        elif self.dir == 315:
            self.dx = 0.7
            self.dy = 0.7
        else:
            print("Es ist was faul im Staate Dänemark: " + str(self.dir))
        self.dx *= self.speed
        self.dy *= self.speed
    
    def checkBounds(self):
        if self.x > WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WIDTH
        if self.y > HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = HEIGHT

# Pygame initialisieren und das Fenster und die Hintergrundfarbe festlegen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

background = pygame.Surface(screen.get_size())
background.fill(BG)
screen.blit(background, (0, 0))

clock = pygame.time.Clock()

ship = Ship(screen)
allSprites = pygame.sprite.Group(ship)

keep_going = True
while keep_going:
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship.turnLeft()
            elif event.key == pygame.K_RIGHT:
                ship.turnRight()
            elif event.key == pygame.K_UP:
                ship.speedUp()
            elif event.key == pygame.K_DOWN:
                ship.slowDown()
            elif event.key == pygame.K_ESCAPE:
                keep_going = False

    allSprites.clear(screen, background)
    allSprites.update()
    allSprites.draw(screen)
    
    pygame.display.flip()

pygame.quit()
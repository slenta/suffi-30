import pygame, asyncio
from pygame.locals import *
import os, sys

# Konstanten deklarieren
WIDTH, HEIGHT = 640, 480
BG_WIDTH = 1664
TITLE = "🐍 Pygame im Browser 🐍"
FPS = 60

# Farben
BG_COLOR = (0, 80, 125)    # Mittelblau

# Klassen
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load Images
        self.images = []
        for i in range (2):
            img = pygame.image.load("data/planegreen_" + str(i) + ".png").convert_alpha()
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.x = 75
        self.y = 250
        self.frame = 0
        self.animation_cycle = 20
        self.animation_time = 4
        self.updown = 5
  
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.y > 20:
                self.y -= self.updown
        elif keys[pygame.K_d]:
            if self.y < HEIGHT - 20:
                self.y += self.updown
        else:
            self.y += 0
        self.rect.center = (self.x, self.y)
        self.animation_cycle += 1
        if self.animation_cycle >= self.animation_time:
            self.animation_cycle = 0
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
        self.image = self.images[self.frame]

class Background(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.x = _x
        self.y = _y
        self.start_x = _x
        self.image = pygame.image.load("data/desert.png")
        self.rect = self.image.get_rect()
        
    def update(self):
        self.x -= 1
        # print(self.x)
        self.rect.x = self.x
        if self.x <= -BG_WIDTH:
            self.x = BG_WIDTH


# Pygame und das Fenster initialisieren
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Sprite-Gruppe(n)
backs       = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Hintergrund
back1 = Background(0, 0)
back2 = Background(BG_WIDTH, 0)
backs.add(back1)
backs.add(back2)

# Der grüne Flieger
plane = Player()
all_sprites.add(plane)

# Hauptschleife
async def main():
    keep_going = True
    while keep_going:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if ((event.type == pygame.QUIT)
                or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE)):
                keep_going = False
                # print("Bye, Bye, Baby!")
                pygame.quit()
                sys.exit()
                               
        screen.fill(BG_COLOR)
        backs.update()
        backs.draw(screen)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        pygame.display.flip()
        
        await asyncio.sleep(0)  # Very important, and keep it 0

asyncio.run(main())
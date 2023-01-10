import pygame
from pygame.locals import *
import os, sys
from random import randint

# Hier wird der Pfad zum Verzeichnis der Assets gesetzt
# DATAPATH = os.path.join(os.getcwd(), "data")
# file_path = os.path.dirname(os.path.abspath(__file__))
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Konstanten deklarieren
WIDTH, HEIGHT = 640, 480
TITLE = "Pizzaplane Startscreen / Trailer"
BG_WIDTH = 1664
FPS = 60

# Farben
BG_COLOR = (231, 229, 226)    # Wüstenhimmel

class Background(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.x = _x
        self.y = _y
        self.start_x = _x
        self.image = pygame.image.load(os.path.join(DATAPATH,
                            "desert.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width = 1664
        
    def update(self):
        self.x -= 1
        # print(self.x)
        self.rect.x = self.x
        if self.x <= -self.bg_width:
            self.x = self.bg_width


class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load Images
        self.image = pygame.image.load(os.path.join(DATAPATH,
                            "pizzaplane_banner.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = 60
        self.y = HEIGHT/2
        self.rect.x = self.x
        self.rect.y = self.y
#         self.frame = 0
#         self.updown = 5
  
    def update(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_UP]:
#             if self.y > 0:
#                 self.y -= self.updown
#         elif keys[pygame.K_DOWN]:
#             if self.y < HEIGHT - 140:
#                 self.y += self.updown
        self.rect.x = self.x
        self.rect.y = self.y

        
class GameWorld:
    
    def __init__ (self):
        # Initialisiert die Spielewelt
        pygame.init()
        # Ein übler Hack, um die Position des Fensters auf meinen zweiten Bildschirm zu setzen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1320, 60)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.keep_going = True
        
    def reset(self):
        # Neustart oder Status zurücksetzen
        # Hier werden alle Elemente der GameWorld initialisiert
        self.backs       = pygame.sprite.Group()
        back1 = Background(0, 0)
        back2 = Background(BG_WIDTH, 0)
        self.backs.add(back1)
        self.backs.add(back2)
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        # Hauptschleife des Spiels
        while self.keep_going:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if ((event.type == pygame.QUIT)
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                keep_going = False
                self.game_over()

    def update(self):
        self.backs.update()
        self.all_sprites.update()
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        self.backs.draw(self.screen)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def start_screen(self):
        pass
    
    def win_screen(self):
        pass
    
    def loose_screen(self):
        pass
    
    def game_over(self):
        print("Bye, Bye, Baby!")
        pygame.quit()
        sys.exit()

# Hauptprogramm
w = GameWorld()
w.start_screen()
w.reset()
w.run()
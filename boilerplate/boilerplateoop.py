import pygame
from pygame.locals import *
import os, sys
from random import randint

# Hier wird der Pfad zum Verzeichnis der Assets gesetzt
DATAPATH = os.path.join(os.getcwd(), "data")

# Konstanten deklarieren
WIDTH, HEIGHT = 640, 480
TITLE = "🐍 Pygame Boilerplate Objektorientiert 🐍"
FPS = 60

# Farben
BG_COLOR = (231, 229, 226) # Sandgrau
           
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
        pass
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        
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
w.run()
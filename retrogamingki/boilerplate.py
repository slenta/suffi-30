import pygame
import os, sys

# Hier wird der Pfad zum Verzeichnis der Assets gesetzt
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Konstanten deklarieren
WIDTH, HEIGHT = 640, 480
TITLE = "🐍 Pygame-CE Boilerplate (OOP) 🐍"
FPS = 60

# Farben
BG_COLOR = (0, 80, 125)    # Mittelblau

# Klassen
# ---------------------------------------------------------------------- #
## Class GameWorld
class GameWorld:
    
    def __init__(self):
        # Pygame und das Fenster initialisieren
        pygame.init()
        # Ein übler Hack, um die Position des Fensters
        # auf meinen zweiten Bildschirm zu setzen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1940, 70)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        
        self.clock = pygame.time.Clock()
        self.keep_going = True
        self.playing = False
        
        # Load Assets
        self.player_im = pygame.image.load(os.path.join(DATAPATH, "pygame_ce_tiny.png")).convert_alpha()
        
    def reset(self):
        # Neustart oder Status zurücksetzen
        # Hier werden alle Elemente der GameWorld initialisiert
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.playing = True
    
    def events(self):
        # Poll for events
        for event in pygame.event.get():
            if ((event.type == pygame.QUIT) or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                if self.playing:
                    self.playing = False
                self.keep_going = False
    
    def update(self):
        self.all_sprites.update()
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Game drawings go here
        self.all_sprites.draw(self.screen)
        
        # Alle Änderungen auf den Bildschirm
        pygame.display.flip()
        
    def start_screen(self):
        pass
    
    def end_screen(self):
        pass
 
# ---------------------------------------------------------------------- #
## Class Player
class Player(pygame.sprite.Sprite):
     
    def __init__(self, _world):
        super().__init__()
        self.game_world = _world
        self.image = self.game_world.player_im
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH/2, HEIGHT/2 - 80
        self.speed = 2
         
    def update(self):
        self.rect.x += self.speed
        # print("update")
        if self.rect.x >= WIDTH:
            self.rect.x = -214           

# Hauptprogramm
world = GameWorld()
world.start_screen()
world.reset()

# Hauptschleife
while world.keep_going:
    world.events()
    world.update()
    world.draw()
    
    # Framerate festsetzen
    world.clock.tick(FPS)
    
pygame.quit()
sys.exit(0)
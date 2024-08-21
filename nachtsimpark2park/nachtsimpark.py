import pygame
import os, sys

# Hier wird der Pfad zum Verzeichnis der Assets gesetzt
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Konstanten deklarieren
TITLE = "Nachts im Park 1"
TS = 8                                # Tile-Size
GRID_X = 30                           # Grid_x = Breite
GRID_Y = 16                           # Grid_y = Höhe
WIDTH, HEIGHT = GRID_X*TS, GRID_Y*TS  # Fenstergröße
SCALE = 3                             # Scale-Factor
FPS = 60

# Tiles
WALL_1 = 63

# Farben
BG_COLOR = (167, 240, 112)            # Light Green

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
        self.screen = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))
        pygame.display.set_caption(TITLE)
        
        self.clock = pygame.time.Clock()
        self.keep_going = True
        self.playing = False
        
        # Load Assets
        self.player_im = pygame.transform.scale_by(pygame.image.load(os.path.join(DATAPATH, "hero1.png")), (SCALE, SCALE)).convert_alpha()
        
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
            if(event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                self.player.dir = "left"
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                self.player.dir = "right"
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                self.player.dir = "up"
            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                self.player.dir = "down"
    
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
        self.pos = [15, 8]
        self.rect.x, self.rect.y = self.pos[0]*TS*SCALE, self.pos[1]*TS*SCALE
        self.dir = "idle"
         
    def update(self):
        if self.dir == "left":
            self.pos[0] -= 1
            self.rect.x = self.pos[0]*TS*SCALE
            self.dir = "none"
        elif self.dir == "right":
            self.pos[0] += 1
            self.rect.x = self.pos[0]*TS*SCALE
            self.dir = "none"
        elif self.dir == "up":
            self.pos[1] -= 1
            self.rect.y = self.pos[1]*TS*SCALE
            self.dir = "none"
        elif self.dir == "down":
            self.pos[1] += 1
            self.rect.y = self.pos[1]*TS*SCALE
            self.dir = "none"
            
            

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

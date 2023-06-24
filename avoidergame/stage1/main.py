# Avoider Game Stage 0.5
import pygame as pg
import asyncio
from pygame.locals import *
from random import randint
import os, sys

## Settings
WIDTH, HEIGHT = 640, 480
TITLE = "Avoider Game, Stage 1"
FPS = 60                   # Frame per second
TW, TH = 36, 36            # Größe der einzelnen Sprites
TW2 = TW // 2
PLAYER_Y = 320
NO_ENEMIES = 7
SPEED_MIN = 2
SPEED_MAX = 7
START_ZONE = 200
DANGER_ZONE = 360

## Hier wird der Pfad zum Verzeichnis der Assets gesetzt
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

## Farben
BG_COLOR = (128, 57, 52)

# Klassen
## Class GameWorld
class GameWorld:

    def __init__(self):
        # Pygame und das Fenster initialisieren
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.keep_going = True

        # Load Assets
        self.skull_image = pg.image.load(os.path.join(DATAPATH, "skull2.png")).convert_alpha()
        self.smiley0_image = pg.image.load(os.path.join(DATAPATH, "smiley0.png")).convert_alpha()
        self.smiley1_image = pg.image.load(os.path.join(DATAPATH, "smiley1.png")).convert_alpha()
        self.smiley2_image = pg.image.load(os.path.join(DATAPATH, "smiley4.png")).convert_alpha()
        self.score_font = pg.font.Font(os.path.join(DATAPATH, "comichelvetic_medium.ttf"), 25)

        # Game State
        self.start_game = True
        self.play_game = False
        self.game_over = False


    def reset(self):
        # Neustart oder Status zurücksetzen
        # Hier werden alle Elemente der GameWorld initialisiert
        self.all_sprites = pg.sprite.Group()
        for _ in range(NO_ENEMIES):
            enemy = Enemy(randint(TW2, WIDTH - TW2), -randint(50, 250), self)
            self.all_sprites.add(enemy)        
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.hud = HUD(self)
          
    def events(self):
        for event in pg.event.get():
            if ((event.type == pg.QUIT)
                or (event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE)):
                if self.playing:
                    self.playing = False
                self.keep_going = False
 
    def update(self):
        self.all_sprites.update()
        self.hud.update(self.player.score)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.hud.score, self.hud.score_rect)
        pg.display.flip()
    
    def start_screen(self):
        pass

    def game_over_screen(self):
        # print("Game Over")
        pass    
## Ende Class GameWorld

## Class Player
class Player(pg.sprite.Sprite):

    def __init__(self, _world):
        super().__init__()
        self.game_world = _world
        self.image = self.game_world.skull_image
        self.rect = self.image.get_rect()
        self.x, self.y = WIDTH/2, PLAYER_Y
        self.score = 0
    
    def update(self):
        x, y = pg.mouse.get_pos()
        if x <= TW2:
            x = TW2
        elif x >= WIDTH - TW2:
            x = WIDTH - TW2
        self.rect.center = (x, self.y)
## End Class Player

## Class Enemy
class Enemy(pg.sprite.Sprite):

    def __init__(self, _x, _y, _world):
        super().__init__()
        self.x, self.y = _x, _y
        self.game_world = _world
        self.image = self.game_world.smiley0_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.dy = randint(SPEED_MIN, SPEED_MAX)
    
    def update(self):
        self.over = False
        self.y += self.dy
        if self.y <= START_ZONE:
            self.image = self.game_world.smiley0_image
        elif self.y <= DANGER_ZONE:
            self.image = self.game_world.smiley1_image
        else:
            self.image = self.game_world.smiley2_image
        self.rect.center = (self.x, self.y)
        if self.rect.top >= HEIGHT:
            self.over = True
            self.game_world.player.score += 1
            # print(self.game_world.player.score)
            self.reset()
    
    def reset(self):
        self.x = randint(TW2, WIDTH - TW2)
        self.y = -randint(50, 250)
        self.rect.center = (self.x, self.y)
        self.dy = randint(SPEED_MIN, SPEED_MAX)

class HUD():

    def __init__(self, _world):
        self.game_world = _world
        self.score_x = 30
        self.score_y = 15
        self.score_font = self.game_world.score_font
        self.score = ""
    
    def update(self, points):
        self.score = self.score_font.render(f"Score: {points}", True, (255, 255, 255))
        self.score_rect = self.score.get_rect()
        self.score_rect.x = self.score_x
        self.score_rect.y = self.score_y

# Hauptprgramm
world = GameWorld()
world.start_screen()

# Hauptschleife
async def main():
    while world.keep_going:
        world.reset()
        world.playing = True
        while world.playing:
            world.clock.tick(FPS)
            world.events()
            world.update()
            world.draw()
            await asyncio.sleep(0)  # Very important, and keep it 0
        world.game_over_screen()
    pg.quit()
    sys.exit()

asyncio.run(main())

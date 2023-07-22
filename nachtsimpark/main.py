# A night in a secret garden
# Kenney Game Jam 2023
# Jörg Kantel
import pygame as pg
import asyncio
from pygame.locals import *
import os, sys
from settings import *

## Class GameWorld
class GameWorld:

    def __init__(self):
        # Pygame und das Fenster initialisieren
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.keep_going = True
        # pg.key.set_repeat(0, 0)


    def reset(self):
        # Neustart oder Status zurücksetzen
        # Hier werden alle Elemente der GameWorld initialisiert
        ## Load Assets
        self.bg_image = pg.image.load(os.path.join(IMAGEPATH, "secretpark.png")).convert_alpha()
        ## Load Walls
        room = room_01
        self.walls = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH - 10):
                if room[y][x] >= 60:
                    self.walls.append((x, y))
        # print(self.walls)
        ## Sprites
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

    def events(self):
        for event in pg.event.get():
            if ((event.type == pg.QUIT)
                or (event.type == pg.KEYDOWN
                and event.key == pg.K_ESCAPE)):
                self.keep_going = False
                self.game_over()
            
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_w or event.key == pg.K_UP):
                    self.player.dy = -1 
                elif (event.key == pg.K_s or event.key == pg.K_DOWN):
                    self.player.dy = 1
                elif (event.key == pg.K_a or event.key == pg.K_LEFT):
                    self.player.dx = -1 
                elif (event.key == pg.K_d or event.key == pg.K_RIGHT):
                    self.player.dx = 1
            
            if event.type == pg.KEYUP:
                self.player.dx, self.player.dy = 0, 0

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.bg_image, (0, 0))
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def game_over(self):
        print("Bye, Bye, Baby!")
        pg.quit()
        sys.exit()
## Ende Class GameWorld

## Class Player
class Player(pg.sprite.Sprite):

    def __init__(self, _world):
        self.world = _world
        super().__init__()
        # Load Image
        img = pg.image.load(os.path.join(IMAGEPATH, "hero.png")).convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()
        self.x, self.y = PLAYER_START_X*GRIDSIZE, PLAYER_START_Y*GRIDSIZE
        self.dx, self.dy = 0, 0

    def update(self):
        if (self.x + self.dx, self.y + self.dy) not in world.walls:
            self.x += self.dx
            self.y += self.dy
        else:
            self.x += 0
            self.y += 0
        self.rect.x, self.rect.y = self.x, self.y

## End Class Player

# Hauptprogramm
world = GameWorld()
world.reset()

# Hauptschleife
async def main():
    while world.keep_going:
        world.clock.tick(FPS)
        world.events()
        world.update()
        world.draw()
        await asyncio.sleep(0)     # Very important, and keep it 0

asyncio.run(main())
# Apple Invaders Stage 1: Player und Plattform

import pygame as pg
from pygame.locals import *  # Wenn dies nicht importiert wird,
                             # kann man UTF-8 (Umlaute) knicken
from settings import *
from sprites import Player, Block
import random
import os

class World:
    
    def __init__ (self):
        # Initialisiert die Spielewelt
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.keep_going = True
    
    def new(self):
        # Initialisieren und/oder Zurücksetzen
        self.all_sprites = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.block1 = Block(0, HEIGHT - 64, WIDTH, 32)
        self.all_sprites.add(self.block1)
        self.blocks.add(self.block1)
        self.block2 = Block(WIDTH/2 - 64, HEIGHT - 192, 128, 32)
        self.all_sprites.add(self.block2)
        self.blocks.add(self.block2)
        self.run()
        
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        # Game-Loop Update
        self.all_sprites.update()
        colls = pg.sprite.spritecollide(self.player, self.blocks, False)
        if colls:
            self.player.pos.y = colls[0].rect.top
            self.player.vel.y = 0
    
    def events(self):
        # Game-Loop Events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.playing:
                    self.playing = False
                self.keep_going = False
  
    def draw(self):
        # Game-Loop Drawkkk
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def splash_screen(self):
        # Start-Screen
        pass
        
    def game_over(self):
        pass
        

w = World()
w.splash_screen()
while w.keep_going:
    w.new()
    w.game_over()
    
pg.quit()
    
    


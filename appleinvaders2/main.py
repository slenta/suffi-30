# Apple Invaders Stage 2: Jumping

import pygame as pg
from settings import Settings
from sprites import Player, Block
import random
import os

class World:
    
    def __init__ (self):
        # Initialisiert die Spielewelt
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        pg.display.set_caption(s.TITLE)
        self.clock = pg.time.Clock()
        self.keep_going = True
    
    def new(self):
        # Initialisieren und/oder Zurücksetzen
        self.all_sprites = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.player = Player(w)
        self.all_sprites.add(self.player)
        for block in s.BLOCKS_LIST:
            b = Block(*block)
            self.all_sprites.add(b)
            self.blocks.add(b)
        self.run()
        
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(s.FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        # Game-Loop Update
        self.all_sprites.update()
        # Nur Kollisionserkennung, wenn der Spieler fällt
        if self.player.vel.y > 0:
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
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_a) or (event.key == pg.K_SPACE):
                    self.player.jump()
  
    def draw(self):
        # Game-Loop Draw
        self.screen.fill(s.BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def splash_screen(self):
        # Start-Screen
        pass
        
    def game_over(self):
        pass
        
s = Settings()
w = World()
w.splash_screen()
while w.keep_going:
    w.new()
    w.game_over()
    
pg.quit()

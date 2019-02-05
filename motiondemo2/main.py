# Natürliche Bewegung mit Beschleunigung und Reibung und langsamen Abbremsen vor den Ecken
import pygame as pg
from settings import *
from sprites import Player
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
        # Initializes and Resets the Game
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
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
    
    def events(self):
        # Game-Loop Events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.playing:
                    self.playing = False
                self.keep_going = False
  
    def draw(self):
        # Game-Loop Draw 
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
    
    


# Sprite Klassen
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    
    def __init__(self, world):
        pg.sprite.Sprite.__init__(self)
        self.world = world
        self.image = pg.Surface((32, 32))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos =vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    
    def jump(self):
        # Nur springen, wenn man auf einem Block steht
        self.rect.x += 1
        colls = pg.sprite.spritecollide(self, self.world.blocks, False)
        self.rect.x -= 1
        if colls:
            self.vel.y = -15
    
    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        # Bewegungsgleichungen
        self.acc.x += self.vel.x*PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
    
        # Randbehandlung
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
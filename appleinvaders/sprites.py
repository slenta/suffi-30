# Sprite Klassen
import pygame as pg
from settings import Settings
vec = pg.math.Vector2

s = Settings()

class Player(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((32, 32))
        self.image.fill(s.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (s.WIDTH/2, s.HEIGHT/2)
        self.pos =vec(s.WIDTH/2, s.HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    
    def update(self):
        self.acc = vec(0, s.PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -s.PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = s.PLAYER_ACC
        
        # Bewegungsgleichungen
        self.acc.x += self.vel.x*s.PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel
    
        # Randbehandlung
        if self.pos.x > s.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = s.WIDTH
        
        self.rect.midbottom = self.pos

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(s.GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
import pygame
from pygame.locals import *
from random import randint
import os
import sys

# Hier wird der Pfad zum Verzeichnis der Assets gesetzt
# DATAPATH = os.path.join(os.getcwd(), "data")
# FONTPATH = os.path.join(os.getcwd(), "fonts")
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FONTPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

# Konstanten deklarieren
WIDTH, HEIGHT = 720, 520
BG_WIDTH = 1664
TITLE = "Pizza Plane Stage 5: Improvements"
FPS = 60
ANIM = 4 # Animation cycle
UPDOWN = 3
NO_ENEMIES = 10

# Farben
BG_COLOR = (231, 229, 226) # Wüstenhimmel

# Objekte
class Background(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.x = _x
        self.y = _y
        self.start_x = _x
        self.image = pygame.image.load(os.path.join(DATAPATH, "desert.png")).convert_alpha()
        self.rect = self.image.get_rect()
        
    def update(self):
        self.x -= 1
        # print(self.x)
        self.rect.x = self.x
        if self.x <= -BG_WIDTH:
            self.x = BG_WIDTH

class Missile(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DATAPATH, "missile.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.speed = 10
        
    def update(self):
        self.rect.x += self.speed
        for enemy in enemies:
            if pygame.sprite.collide_rect(enemy, self):
                self.kill()
                # enemy.kill()
                e_x, e_y = enemy.rect.x, enemy.rect.y - 5
                enemy.reset()
                hit = Explosion(e_x, e_y)
                all_sprites.add(hit)
                plane.score += 10
        if self.rect.x >= WIDTH + 20:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DATAPATH, "explosion.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.timer = 5
        
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()        

class  Plane(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load Images
        self.images = []
        for i in range (2):
            img = pygame.image.load(os.path.join(DATAPATH, f"planegreen_{i}.png")).convert_alpha()
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.x = 75
        self.y = 250
        self.frame = 0
        self.ani = 20
        self.dir = "NONE"
        self.firecount = 0
        self.score = 0
        self.lives = 5
    
    def update(self):
        if self.dir == "NONE":
            self.y += 0
        elif self.dir == "UP":
            if self.y > 20:
                self.y -= UPDOWN
        elif self.dir == "DOWN":
            if self.y < HEIGHT - 20:
                self.y += UPDOWN
        self.rect.center = (self.x, self.y)
        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                enemy.reset()
                self.lives -= 1
                if self.lives < 0:
                    print(f"Verloren! (Score: {self.score} Punkte).")
                    pygame.quit()
                    try:
                        sys.exit()
                    finally:
                        keep_going = False
        self.ani += 1
        if self.ani >= ANIM:
            self.ani = 0
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
        self.firecount -= 1
        self.image = self.images[self.frame]
        
    def fire(self):
        if self.firecount < 0:
            missile = Missile(self.x + 15, self.y)
            all_sprites.add(missile)
            self.firecount = 15

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DATAPATH, "pizza.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.speed = randint(3, 6)
        
    def reset(self):
        self.rect.x = WIDTH + randint(30, 100)
        self.rect.y = randint(30, HEIGHT - 30)
        self.speed = randint(3, 6)
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -30:
            self.reset()
            plane.score -= 2
            if plane.score < 0:
                print("Zu viele Pizzas entkommen lassen!")
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    keep_going = False

class Peppi(Enemy):
    
    def __init__(self, _x, _y):
        Enemy.__init__(self, _x, _y)
        self.image = pygame.image.load(os.path.join(DATAPATH, "peppi.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.speed = randint(6, 9)
    
    def reset(self):
        self.rect.x = WIDTH + randint(30, 100)
        self.rect.y = randint(30, HEIGHT - 30)
        self.speed = randint(6, 9)
        
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -30:
            self.reset()
            plane.score -= 2
            if plane.score < 0:
                print("Zu viele Pizzas entkommen lassen!")
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    keep_going = False


class HUD():
    
    def __init__(self):
        self.score_x = WIDTH - 170
        self.score_y = 15
        self.heart_x = 30
        self.heart_y = 20
        # Load Fonts
        self.score_font = pygame.font.Font(os.path.join(FONTPATH, "RubikGemstones-Regular.ttf"), 25)
        self.score = ""
        # Load Hearts
        self.score_live = "Lifes :" 
        self.heart_img = pygame.image.load(os.path.join(DATAPATH, "heart.png")).convert_alpha()
        self.heart_rect = self.heart_img.get_rect()
        
        
    def update(self, points):
        self.score = self.score_font.render(f"Score: {points}", True, (0, 0, 0))
        self.score_rect = self.score.get_rect()
        self.score_rect.x = self.score_x
        self.score_rect.y = self.score_y
        self.score_lives = self.score_font.render("Lives: ", True, (0, 0, 0))
        self.score_lives_rect = self.score_lives.get_rect()
        self.score_lives_rect.x = self.heart_x
        self.score_lives_rect.y = self.score_y
        
           
# Pygame initialisieren und das Fenster und die Hintergrundfarbe festlegen
clock = pygame.time.Clock()
pygame.init()
# Ein übler Hack, um die Position des Fensters auf meinen zweiten Bildschirm zu setzen,
# aber er funktioniert …
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1320, 60)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Sprite-Gruppe(n)
backs       = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemies     = pygame.sprite.Group()

# Hintergrund
back1 = Background(0, 0)
back2 = Background(BG_WIDTH, 0)
backs.add(back1)
backs.add(back2)

# Head Up Display
hud = HUD()

# Die Gegner
for _ in range(NO_ENEMIES):
    change = randint(1, 3)
    if change <= 2:
        pizza = Enemy(WIDTH + randint(30, 100), randint(30, HEIGHT - 30))
        all_sprites.add(pizza)
        enemies.add(pizza)
    else:
        peppi = Peppi(WIDTH + randint(30, 100), randint(30, HEIGHT - 30))
        all_sprites.add(peppi)
        enemies.add(peppi)


# Der Flieger
plane = Plane()
all_sprites.add(plane)

keep_going = True
while keep_going:
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT)
            or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            print("Bye, Bye, Baby!")
            pygame.quit()
            try:
                sys.exit()
            finally:
                keep_going = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                plane.dir = "UP"
            elif event.key == pygame.K_DOWN:
                plane.dir = "DOWN"
            if event.key == pygame.K_RIGHT:
                plane.fire()
                
        if event.type == pygame.KEYUP:
            plane.dir = "NONE"

    backs.update()
    backs.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    hud.update(plane.score)
    screen.blit(hud.score, hud.score_rect)
    screen.blit(hud.score_lives, (hud.score_lives_rect.x, hud.score_lives_rect.y))
    for i in range(plane.lives):
        hud.heart_rect.x = hud.score_lives_rect.right + 10 + i*(hud.heart_img.get_width() + 10)
        screen.blit(hud.heart_img, (hud.heart_rect.x, hud.heart_y))
    pygame.display.update()
    pygame.display.flip()

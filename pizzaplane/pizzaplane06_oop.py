import pygame
from pygame.locals import *
import os, sys
from random import randint

# Hier wird der Pfad zum Verzeichnis der Assets gesetzt
# DATAPATH = os.path.join(os.getcwd(), "data")
# file_path = os.path.dirname(os.path.abspath(__file__))
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FONTPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

# Konstanten deklarieren
WIDTH, HEIGHT = 720, 520
BG_WIDTH = 1664
TITLE = "Pizzaplane Objektorientiert"
FPS = 60

NO_ENEMIES = 10

# Farben
BG_COLOR = (231, 229, 226)    # Wüstenhimmel

class Background(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.x = _x
        self.y = _y
        self.start_x = _x
        self.image = pygame.image.load(os.path.join(DATAPATH,
                            "desert.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.bg_width = 1664
        
    def update(self):
        self.x -= 1
        # print(self.x)
        self.rect.x = self.x
        if self.x <= -self.bg_width:
            self.x = self.bg_width

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
        for enemy in w.enemies:
            if pygame.sprite.collide_rect(enemy, self):
                self.kill()
                # enemy.kill()
                e_x, e_y = enemy.rect.x, enemy.rect.y - 5
                enemy.reset()
                hit = Explosion(e_x, e_y)
                w.all_sprites.add(hit)
                w.plane.score += 10
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

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load Images
        self.images = []
        for i in range (2):
            img = pygame.image.load(os.path.join(DATAPATH,
                         "planegreen_" + str(i) + ".png")).convert_alpha()
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.x = 75
        self.y = 250
        self.frame = 0
        self.animation_cycle = 20
        self.animation_time = 4
        self.updown = 5
        self.firecount = 0
        self.score = 0
        self.lives = 5

  
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.y > 20:
                self.y -= self.updown
        elif keys[pygame.K_DOWN]:
            if self.y < HEIGHT - 20:
                self.y += self.updown
        else:
            self.y += 0
        if keys[pygame.K_RIGHT]:
            self.fire()

        self.rect.center = (self.x, self.y)
        self.animation_cycle += 1
        if self.animation_cycle >= self.animation_time:
            self.animation_cycle = 0
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
        self.image = self.images[self.frame]
        
        self.firecount -= 1

    def fire(self):
        if self.firecount < 0:
            missile = Missile(self.x + 15, self.y)
            w.all_sprites.add(missile)
            self.firecount = 15

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(DATAPATH, "pizza.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        
    def reset(self):
        self.rect.x = WIDTH + randint(30, 100)
        self.rect.y = randint(30, HEIGHT - 30)

    def update(self):
        if self.rect.x < -30:
            self.reset()
            w.plane.score -= 2


class Pizza(Enemy):
    
    def __init__(self, _x, _y):
        Enemy.__init__(self, _x, _y)
        self.image = pygame.image.load(os.path.join(DATAPATH, "pizza.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.speed = 3    # randint(3, 6)
    
    def reset(self):
        Enemy.reset(self)
        self.speed = randint(3, 6)
        
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -30:
            self.reset()
            w.plane.score -= 2

class Peppi(Enemy):
    
    def __init__(self, _x, _y):
        Enemy.__init__(self, _x, _y)
        self.image = pygame.image.load(os.path.join(DATAPATH, "peppi.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.speed = randint(6, 9)
        
    def reset(self):
        Enemy.reset(self)
        self.speed = randint(6, 9)
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -30:
            self.reset()
            w.plane.score -= 2

class GameWorld:
    
    def __init__ (self):
        # Initialisiert die Spielewelt
        pygame.init()
        # Ein übler Hack, um die Position des Fensters auf meinen zweiten Bildschirm zu setzen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1320, 60)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.keep_going = True
        
    def reset(self):
        # Neustart oder Status zurücksetzen
        # Hier werden alle Elemente der GameWorld initialisiert
        self.backs = pygame.sprite.Group()
        back1 = Background(0, 0)
        back2 = Background(BG_WIDTH, 0)
        self.backs.add(back1)
        self.backs.add(back2)
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies     = pygame.sprite.Group()
        
        # Head Up Display
        self.hud = HUD()
        
        # Die Gegner
        for _ in range(NO_ENEMIES):
            change = randint(1, 3)
            if change <= 2:
                pizza = Pizza(WIDTH + randint(30, 100), randint(30, HEIGHT - 30))
                self.all_sprites.add(pizza)
                self.enemies.add(pizza)
            else:
                peppi = Peppi(WIDTH + randint(30, 100), randint(30, HEIGHT - 30))
                self.all_sprites.add(peppi)
                self.enemies.add(peppi)
        
        # Der Spieler
        self.plane = Player()
        self.all_sprites.add(self.plane)
        self.run()

    def run(self):
        # Hauptschleife des Spiels
        while self.keep_going:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if ((event.type == pygame.QUIT)
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                keep_going = False
                self.game_over()

    def update(self):
        self.backs.update()
        self.all_sprites.update()
        self.hud.update(self.plane.score)
    
    def draw(self):
        # Hintergrund zeichnen und animieren
        self.screen.fill(BG_COLOR)
        self.backs.draw(self.screen)
        # Den Flieger und seine Gegner
        self.all_sprites.draw(self.screen)
        # Punkteanzeige
        self.screen.blit(self.hud.score, self.hud.score_rect)
        self.screen.blit(self.hud.score_lives, (self.hud.score_lives_rect.x, self.hud.score_lives_rect.y))
        for i in range(self.plane.lives):
            self.hud.heart_rect.x = self.hud.score_lives_rect.right + 10 \
                                    + i*(self.hud.heart_img.get_width() + 10)
            self.screen.blit(self.hud.heart_img, (self.hud.heart_rect.x, self.hud.heart_y))

        pygame.display.flip()

    def start_screen(self):
        pass
    
    def win_screen(self):
        pass
    
    def loose_screen(self):
        pass
    
    def game_over(self):
        print("Bye, Bye, Baby!")
        pygame.quit()
        sys.exit()

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

# Hauptprogramm
w = GameWorld()
w.start_screen()
w.reset()
w.run()

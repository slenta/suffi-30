import pgzrun
from random import randint
import os

TITLE = "Balloon Flight"
WIDTH = 800
HEIGHT = 600

# Hier wird der Pfad zum Verzeichnis des ».py«-Files gesetzt
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


balloon = Actor("balloon")
balloon.pos = 400, 300
bird = Actor("bird-up")
bird.pos = randint(800, 1600), randint(10, 200)
house = Actor("house")
house.pos = randint(800, 1600), 460
tree = Actor("tree")
tree.pos = randint(800, 1600), 450

bird_up = True
up = False
game_over = False
score = 0
frames = 0

scores = []

def update_high_scores():
    pass

def display_high_scores():
    pass

def draw():
    screen.blit("background", (0, 0))
    if not game_over:
        balloon.draw()
        bird.draw()
        house.draw()
        tree.draw()
        screen.draw.text("Punkte: " + str(score), (700, 5), color = "black")
    else:
        display_high_scores()

def update():
    global game_over, score, frames
    if not game_over:
        if not up:
            
            # Balloon = Player
            balloon.y += 1
            if balloon.top < 0 or balloon.bottom > 560:
                game_over = True
                update_high_scores()
            if balloon.collidepoint(bird.x, bird.y) or \
               balloon.collidepoint(house.x, house.y) or \
               balloon.collidepoint(tree.x, tree.y):
                game_over = True
                update_high_scores()
            
            # Bird
            if bird.x > -bird.width:
                bird.x -= 4
                if frames == 9:
                    flap()
                    frames = 0
                else:
                    frames += 1
            else:
                bird.x = randint(800, 1600)
                bird.y = randint(10, 200)
                score += 1
                frames = 0
            
            # House
            if house.x > -house.width:
                house.x -= 2
            else:
                house.x = randint(800, 1600)
            
            # Tree
            if tree.x > -tree.width:
                 tree.x -= 2
            else:
                 tree.x = randint(800, 1600)
        

def on_mouse_down():
    global up
    up = True
    balloon.y -= 50

def on_mouse_up():
    global up
    up = False

def flap():
    global bird_up
    if bird_up:
        bird.image = "bird-down"
        bird_up = False
    else:
        bird.image = "bird-up"
        bird_up = True

pgzrun.go()
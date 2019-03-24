import pgzrun
from random import randint

WIDTH = 640
HEIGHT = 480
TITLE = "Cute Space"

octopussy = Actor("octopussy", center = (100, HEIGHT/2))

rocketboys = []
for _ in range(3):
    rocketboys.append(Actor("rocketboy", center = (randint(700, 1400), randint(40, 440))))

for rocketboy in rocketboys:
    rocketboy.speed = randint(2, 4)

planets = []
for i in range(2):
    planets.append(Actor("planet", center = (randint(700, 1400), randint(40, 440))))


score = 0
game_over = False

def reset(actor):
    actor.x = randint(700, 1400)
    actor.y = randint(40, 440)

def draw():
    screen.fill((0, 80, 125))
    for planet in planets:
        planet.draw()
    for rocketboy in rocketboys:
        rocketboy.draw()
    octopussy.draw()

def update():
    global game_over, score
    if not game_over:
        octopussy.y += 0
        for rocketboy in rocketboys:
            if rocketboy.x > -rocketboy.width:
                rocketboy.x -= rocketboy.speed
            else:
                reset(rocketboy)
        for planet in planets:
            if planet.x > -planet.width:
                planet.x -= 0.25 
            else:
                reset(planet)
    
def on_mouse_down():
    pass
    
pgzrun.go()

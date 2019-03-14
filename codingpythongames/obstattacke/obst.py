import pgzrun
from random import randint

TITLE = "🍎🍏 Obstattacke 🍏🍎"
WIDTH = 400
HEIGHT = 400

apple = Actor("apple")

def draw():
    screen.clear()
    apple.draw()

def place_apple():
    apple.x = randint(20, WIDTH - 20)
    apple.y = randint(20, HEIGHT - 20)
    
def on_mouse_down(pos):
    if apple.collidepoint(pos):
        print("Treffer")
        place_apple()
    else:
        print("Daneben")
        quit()

place_apple()

pgzrun.go()
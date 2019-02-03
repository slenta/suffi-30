# Konstanten und Einstellungen für das Spiel
import pygame as pg

# Einige nützliche Konstanten
TITLE = "Apple Invaders Stage 2: Jumping"
WIDTH = 640
HEIGHT = 480
FPS = 60   # Framerate

# Player Eigenschaften
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.4

# Blocks Eigenschaften
BLOCKS_LIST = [(0, HEIGHT - 64, WIDTH, 32),
               (WIDTH/2 - 64, HEIGHT - 192, 128, 32)
               ]

# Nützliche Farbdefinitionen 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (160, 160, 160)
LEIGHTGREY = (100, 100, 100)
DARKGREY = (51, 51, 51)
VERY_DARKGREY = (40, 40, 40)
LIGHTBLUE = (108, 131, 163)
WATERBLUE = (0, 80, 125)
AQUA = (0, 153, 204)
BROWN = (163, 143, 109)
LIGHTBROWN = (210, 180, 140)

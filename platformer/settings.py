import os
import pygame as pg

## Settings
GRIDSIZE = 18
GRID_WIDTH = 40
GRID_HEIGHT = 15
WIDTH, HEIGHT = GRID_WIDTH * GRIDSIZE, GRID_HEIGHT * GRIDSIZE
TITLE = "suffisuffzich 3000"
FPS = 60  # Frames per second
PLAYER_WIDTH = 24
PLAYER_HEIGHT = 24
PLAYER_START_X, PLAYER_START_Y = 5, 1
PLAYER_SPEED = 3
BULLET_SPEED = 6

# Physikalische Konstanten
GRAVITY = 0.5
MAX_VELOCITY = 18
JUMP_POWER = 10

## Hier wird der Pfad zum Verzeichnis der Assets gesetzt
IMAGEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/images")

## Farben
BG_COLOR = (65, 166, 246)  # Himmelblau

# Centralized keybindings (use pygame key constants)
# Change these to rebind controls project-wide.
KEYBINDINGS = {
	"left": pg.K_LEFT,
	"right": pg.K_RIGHT,
	"jump": pg.K_UP,
	# Action keys
	"shoot": pg.K_f,  # shoot bullet (F)
	"throw": pg.K_e,  # throw exploding object (E)
	"quit": pg.K_ESCAPE,
}

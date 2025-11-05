"""
Game settings and configuration.
All game-wide settings, constants, and configurations.
"""
import os
import pygame as pg

# === Display Settings ===
GRIDSIZE = 18
GRID_WIDTH = 40
GRID_HEIGHT = 15
WIDTH, HEIGHT = GRID_WIDTH * GRIDSIZE, GRID_HEIGHT * GRIDSIZE
TITLE = "suffisuffzich 3000"
FPS = 60

# === Player Settings ===
PLAYER_WIDTH = 24
PLAYER_HEIGHT = 24
PLAYER_START_X, PLAYER_START_Y = 5, 1
PLAYER_SPEED = 3

# === Weapon Settings ===
BULLET_SPEED = 6

# === Physics Constants ===
GRAVITY = 0.5
MAX_VELOCITY = 18
JUMP_POWER = 10

# === Asset Paths ===
IMAGEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/images")

# === Colors ===
BG_COLOR = (65, 166, 246)  # Sky blue

# === Keybindings ===
# Centralized keybindings using pygame key constants
KEYBINDINGS = {
    "left": pg.K_LEFT,
    "right": pg.K_RIGHT,
    "jump": pg.K_UP,
    "shoot": pg.K_f,
    "throw": pg.K_e,
    "quit": pg.K_ESCAPE,
}

# === Cheat Code Settings ===
CHEAT_CODE = "mfg"  # Activates Marvin Mode

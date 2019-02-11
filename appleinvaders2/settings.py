# Konstanten und Einstellungen für das Spiel
import pygame as pg

class Settings():

    def __init__(self):

        # Einige nützliche Konstanten
        self.TITLE = "🍎 Apple Invaders 🍏 Stage 2: Jumping"
        self.WIDTH = 640
        self.HEIGHT = 480
        self.FPS = 60   # Framerate
        self.TILESIZE = 32

        # Player Eigenschaften
        self.PLAYER_ACC = 0.5
        self.PLAYER_FRICTION = -0.12
        self.PLAYER_GRAV = 0.4

        # Block Eigenschaften
        self.BLOCKS_LIST = [(0, self.HEIGHT - 64, self.WIDTH, 32),
               (self.WIDTH/2 - 64, self.HEIGHT - 192, 128, 32),
               (0, self.HEIGHT - 192, 128, 32),
               (self.WIDTH - 128, self.HEIGHT - 192, 128, 32)
               ]

        # Nützliche Farbdefinitionen 
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GREY = (160, 160, 160)

# Konstanten und Einstellungen für das Spiel
import pygame as pg

class Settings():
    
    def __init__(self):

        # Einige nützliche Konstanten
        self.TITLE = "🐍 Hällo Pygäme! 🐍"
        self.WIDTH = 640
        self.HEIGHT = 480
        self.FPS = 60   # Framerate

        # Nützliche Farbdefinitionen 
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GREY = (160, 160, 160)
        self.LEIGHTGREY = (100, 100, 100)
        self.DARKGREY = (51, 51, 51)
        self.VERY_DARKGREY = (40, 40, 40)
        self.LIGHTBLUE = (108, 131, 163)
        self.WATERBLUE = (0, 80, 125)
        self.AQUA = (0, 153, 204)
        self.BROWN = (163, 143, 109)
        self.LIGHTBROWN = (210, 180, 140)

import pgzrun
import time, random, math

# Konstanten
TITLE = "Spacewalk 3 (Game-Map)"
WIDTH = 800
HEIGHT = 800
TILE_SIZE = 30
PLAYER_NAME = "Jörg"
FRIEND1_NAME = "Zebu"
FRIEND2_NAME = "Joey"

DEMO_OBJECTS = [images.floor, images.pillar, images.soil]

# Karten-Daten
MAP_WIDTH = 5
MAP_HEIGHT = 10
MAP_SIZE = MAP_WIDTH*MAP_HEIGHT

GAME_MAP = [["Raum 0 – wo unnützes Zeug aufbewahrt wird", 0, 0, False, False]]

outdoor = range(1, 26) # Sektor 1 bis Sektor 25
for planetsectors in outdoor:
    GAME_MAP.append( ["Die staubige Planetenpberfläche", 13, 13, True, True])

GAME_MAP += [
        # ["Raum-Name", height, width, Top Exit? Right Exit]
        ["Luftschleuse", 13, 5, True, False], # Raum 26
        ["Konstruktionslabor", 13, 13, False, False], # Raum 27
        ["Pudel?-Kontrollraum", 9, 13, False, True], # Raum 28
        ["Aussichtsraum", 9, 15, False, False], # Raum 29
        ["Gemeinschaftsduschen", 5, 5, False, False], # Raum 30
        ["Vorraum zur Luftschleuse", 7, 11, True, True], # Raum 31
        ["Linker Vorbereitungsraum", 9, 7, True, False], # Raum 32
        ["Rechter Vorbereitungsraum", 7, 13, True, True], # Raum 33
        ["Wissenschaftslabor", 13, 13, False, True], # Raum 34
        ["Gewächshaus", 13, 13, True, False], # Raum 35
        [PLAYER_NAME + "s Schlafzimmer", 9, 11, False, False], # Raum 36
        ["Westlicher Flur", 15, 5, True, True], # Raum 37
        ["Besprechungszimmer", 7, 13, False, True], # Raum 38
        ["Gemeinschaftsraum", 11, 13, True, False], # Raum 39
        ["Kontrollzentrum", 14, 14, False, False], # Raum 40
        ["Krankenstation", 12, 7, True, False], # Raum 41
        ["Westlicher Flur", 9, 7, True, False], # Raum 42
        ["Leitwarte", 9, 9, False, True], # Raum 43
        ["Systemtechnik", 9, 11, False, False], # Raum 44
        ["Sicherheitsportal zum Kontrollzentrum", 7, 7, True, False], # Raum 45
        [FRIEND1_NAME + "s Schlafzimmer", 9, 11, True, True], # Raum 46
        [FRIEND2_NAME + "s Schlafzimmer", 9, 11, True, True], # Raum 47
        ["Raum mit Rohrleitungen", 13, 11, True, False], # Raum 48
        ["Büro des Chefingenieurs", 9, 7, True, True], # Raum 49
        ["Roboterwerkstatt", 9, 11, True, False] # Raum 50
    ]

assert len(GAME_MAP) - 1 == MAP_SIZE, "Kartengröße GAME_MAP stimmen nicht überein"

# Variablen
top_left_x = 100
top_left_y = 150
current_room = 31

def draw():
    pass


pgzrun.go()
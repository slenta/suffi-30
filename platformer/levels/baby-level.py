level_config = {
    "x_bounds": [-100, 1200],  # Kurzes Tutorial-Level
    "y_bounds": [-200, 300],
    "level_time": 60,  # Time limit in seconds (1 minute - it's a short tutorial)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    # "player_spawn": (5, 1),  # Example: spawn at grid position (5, 1)
    # Einfache flache Plattform mit kleinem Loch zum Springen üben
    "grass_locations": [(i, 14) for i in range(-5, 15)]  # Start-Plattform
    + [(i, 14) for i in range(18, 50)],  # Haupt-Plattform (Loch bei 15-17)
    # Paar Blöcke zum Springen üben
    "block_locations": [
        (10, 12),
        (11, 12),
        (25, 10),
        (26, 10),
        (40, 8),
    ],
    # Keine Gems (Tutorial-Level)
    "gem_locations": [],
    # Power-Ups
    "powerup_locations": [
        {"x": 15, "y": 13, "type": "bigger"},  # Babybrei (macht größer)
        {"x": 35, "y": 13, "type": "bigger"},  # Zweiter Babybrei
    ],
    # Waffen
    "weapon_locations": [
        {"x": 8, "y": 13, "type": "milchflasche"},  # Erste Waffe
    ],
    # Gegner
    "enemy_locations": [
        {
            "x": 45,
            "y": 13,
            "image": "enemies/baby-erzieherin.png",  # Boss
            "speed": 1,
            "patrol_range": 100,
            "size_multiplier": 3,
            "health": 20,
            "damage": 5,
            "shoot_range": 0,  # Nur Melee
            "chase_range": 8,
            "melee_damage": 10,
            "can_throw_explosives": False,
        },
    ],
    # Trophies (nur 1 für Tutorial)
    "trophy_locations": [
        (30, 13),
    ],
    "trophy_image": "trophy.png",  # Path relative to assets/images
    # Exit
    "exit_location": (48, 13),
    # Assets
    "background_music": "assets/music/baby_level.ogg",
    "background_image": "assets/backgrounds/kindergarten_bg.png",
    "background_scroll_speed": 0.2,
}

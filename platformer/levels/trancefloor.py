level_config = {
    "x_bounds": [-300, 9000],  # Extended gameworld width (doubled)
    "y_bounds": [-400, 400],  # Increased gameworld height for more vertical space
    "level_time": 300,  # Time limit in seconds (5 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    # "player_spawn": (160, 1),  # Example: spawn at grid position (5, 1)
    # Extended grass locations - keeping original and adding more sections
    "grass_locations": [(i, 14) for i in range(-20, 16)]
    + [(i, 14) for i in range(25, 30)]
    + [(i, 14) for i in range(40, 59)]
    + [(i, 14) for i in range(78, 99)]
    + [(i, 14) for i in range(113, 170)]
    + [(i, 14) for i in range(180, 220)]
    + [(i, 14) for i in range(225, 280)]  # New section 3
    + [(i, 14) for i in range(285, 350)]  # New section 4
    + [(i, 14) for i in range(360, 420)],  # Final section
    # Extended block locations - original plus new challenging platforming sections
    "block_locations": [
        (15, 13),
        (16, 12),
        (17, 11),
        (18, 10),
        (19, 9),
        (20, 8),
        (21, 9),
        (22, 10),
        (23, 11),
        (24, 12),
        (25, 13),
        # pyramid structure
        # abgrund
        (33, 10),
        (34, 10),
        (35, 10),
        # first gem
        (45, 10),
        (46, 10),
        (49, 7),
        (50, 7),
        (43, 3),
        # 2. abgrund
        (60, 10),
        (61, 10),
        (64, 6),
        (65, 6),
        (68, 2),
        (69, 3),
        (70, 4),
        (71, 5),
        (72, 6),
        (73, 7),
        (74, 8),
        (75, 9),
        # first trophy
        (77, 1),
        (78, 1),
        (79, 1),
        (80, 1),
        (81, 1),
        (82, 1),
        (83, 1),
        (84, 1),
        # höhle für powerup type 2
        (82, 11),
        (83, 11),
        (84, 11),
        (85, 11),
        (86, 11),
        # (89, 12),
        # (89, 13),
        (89, 11),
        (89, 10),
        (89, 9),
        (89, 8),
        (88, 8),
        (87, 8),
        (86, 8),
        (85, 8),
        (85, 1),
        (86, 1),
        (87, 1),
        (88, 1),
        (89, 1),
        (90, 1),
        (91, 1),
        (92, 1),
        (93, 1),
        (94, 1),
        (95, 1),
        # (84, 8),
        # (83, 8),
        (82, 8),
        (82, 9),
        (82, 10),
        (82, 7),
        (82, 6),
        (82, 5),
        (83, 5),
        (84, 5),
        (85, 5),
        (86, 5),
        (87, 5),
        (88, 5),
        (89, 5),
        (92, 8),
        # Towers Abgrund
        (103, 13),
        (103, 12),
        (103, 11),
        (103, 10),
        (108, 13),
        (108, 12),
        (108, 11),
        (108, 10),
        # Next gem
        (145, 9),
        (147, 8),
        (149, 7),
        (151, 6),
        # New Jesus Block
        (175, 3),
        (175, 2),
        (175, 1),
        # Trphy
        # (168, 12),
        # (169, 7),
        # (170, 2),
        # Hippie Enemy
        (190, 8),
        (191, 8),
        (192, 8),
        (193, 8),
        (194, 8),
        (195, 8),
        (196, 8),
        (197, 8),
        (198, 8),
        (199, 8),
        (200, 8),
        # Section 6 - Complex structure
        (250, 13),
        (251, 13),
        (252, 13),
        (250, 10),
        (252, 10),
        (251, 7),
        (253, 7),
        (255, 7),
        (254, 4),
        (256, 4),
        # Section 7 - Moving platform bases
        (270, 12),
        (272, 10),
        (274, 8),
        (276, 6),
        # Section 8 - Pyramid structure
        (320, 13),
        (321, 13),
        (322, 13),
        (323, 13),
        (324, 13),
        (321, 10),
        (322, 10),
        (323, 10),
        (322, 7),
        # Section 9 - Final challenge platforms
        (380, 11),
        (382, 9),
        (384, 7),
        (386, 5),
        (388, 3),
        (395, 13),
        (396, 13),
        (397, 13),
        (398, 13),
        # Section 10 - Boss area platforms
        (410, 10),
        (412, 10),
        (414, 10),
        (416, 10),
    ],
    # Extended gem locations - more rewards throughout the longer level
    "gem_locations": [
        # Original gems
        (12, 12),
        (13, 12),
        (14, 12),
        (35, 0),
        (151, 5),
        (195, 13),
    ],
    "powerup_locations": [
        {"x": 83, "y": 3, "type": 2},
        {"x": 108, "y": 5, "type": 0},
        {"x": 10, "y": 10, "type": 3},
    ],
    "enemy_locations": [
        {
            "x": 40,
            "y": 7,
            "image": "enemies/trance-totem.png",
            "speed": 1,
            "patrol_range": 20,
            "size_multiplier": 4,
            "health": 15,
            "damage": 5,
            "shoot_range": 0,
            "chase_range": 10,
            "melee_damage": 2,
            "can_throw_explosives": False,
        },
        {
            "x": 140,
            "y": 7,
            "image": "enemies/trance-totem.png",
            "speed": 1,
            "patrol_range": 20,
            "size_multiplier": 4,
            "health": 15,
            "damage": 5,
            "shoot_range": 0,
            "chase_range": 10,
            "melee_damage": 2,
        },
        {
            "x": 165,
            "y": 10,
            "image": "enemies/trance-jesus.png",
            "speed": 3,
            "patrol_range": 150,
            "size_multiplier": 4,
            "health": 20,
            "damage": 15,
            "shoot_range": 30,
            "chase_range": 20,
            "melee_damage": 10,
        },
        {
            "x": 195,
            "y": 4,
            "image": "enemies/trance-hippie.png",
            "speed": 1,
            "patrol_range": 30,
            "size_multiplier": 4,
            "health": 20,
            "damage": 15,
            "shoot_range": 30,
            "chase_range": 10,
            "melee_damage": 10,
        },
        {
            "x": 240,
            "y": 10,
            "image": "enemies/trance-okf.png",
            "speed": 1,
            "patrol_range": 30,
            "size_multiplier": 4,
            "health": 20,
            "damage": 15,
            "shoot_range": 30,
            "chase_range": 10,
            "melee_damage": 10,
        },
    ],
    # Extended trophy locations - more collectibles
    "weapon_locations": [
        {"x": 175, "y": 0, "type": "wasserpistole"},  # Erste Waffe
    ],
    # Moving platform locations - new feature!
    "moving_platform_locations": [
        {
            "x": 170,  # Starting x position (grid units)
            "y": 4,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 7,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        # {
        #     "x": 60,
        #     "y": 8,
        #     "platform_type": "grass",
        #     "movement_type": "linear",
        #     "speed": 2,
        #     "distance": 8,
        #     "direction": "vertical",
        # },
        # {
        #     "x": 100,
        #     "y": 9,
        #     "platform_type": "block",
        #     "movement_type": "linear",
        #     "speed": 1.5,
        #     "distance": 15,
        #     "direction": "horizontal",
        # },
        {
            "x": 180,
            "y": 9,
            "platform_type": "block",
            "movement_type": "circular",
            "speed": 30,
            "distance": 5,  # This acts as radius for circular movement
            "direction": "horizontal",  # Not used for circular
        },
        # {
        #     "x": 365,
        #     "y": 8,
        #     "platform_type": "block",
        #     "movement_type": "linear",
        #     "speed": 2,
        #     "distance": 12,
        #     "direction": "horizontal"
        # },
    ],
    "trophy_locations": [
        (84, 0),
    ],
    "trophy_image": "mushroom.png",
    "exit_location": (420, 13),
    "background_music": "assets/music/default.ogg",
    # "background_image": "assets/backgrounds/level2.png",
    "background_scroll_speed": 0.2,
    "alternative_backgrounds": [
        "assets/backgrounds/trancefloor.png",
    ],
    "alternative_music_tracks": [
        "assets/music/trancefloor.ogg",
    ],
}

level_config = {
    "x_bounds": [-300, 9000],  # Extended gameworld width (doubled)
    "y_bounds": [-1200, 1200],  # Increased gameworld height for more vertical space
    "level_time": 300,  # Time limit in seconds (5 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    "player_spawn": (238, 12),  # Example: spawn at grid position (5, 1)
    # Extended grass locations - keeping original and adding more sections
    "grass_locations": [(i, 14) for i in range(-20, 16)]
    + [(i, 14) for i in range(25, 30)]
    + [(i, 14) for i in range(40, 59)]
    + [(i, 14) for i in range(78, 99)]
    + [(i, 8) for i in range(112, 150)]
    + [(i, -2) for i in range(150, 175)]
    + [(i, -2) for i in range(180, 190)]
    + [(i, -2) for i in range(193, 203)]
    + [(i, -2) for i in range(206, 218)]
    + [(i, 14) for i in range(225, 240)]
    + [(240, i) for i in range(14, 22)]
    + [(i, 22) for i in range(240, 285)]
    + [(270, i) for i in range(14, 20)]
    + [(i, 14) for i in range(270, 281)]
    + [(i, 14) for i in range(282, 350)]
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
        (42, 3),
        (49, -2),
        (48, -2),
        (47, -2),
        (54, -5),
        (55, -5),
        (48, -9),
        (47, -9),
        (46, -9),
        (45, -9),
        (44, -9),
        (43, -9),
        (42, -9),
        (41, -9),
        (40, -9),
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
        (136, -1),
        (134, 0),
        (132, 1),
        (130, 2),
        (128, 3),
        # First Weapon
        (159, -14),
        (160, -14),
        (161, -14),
        # Hippie Enemy
        (210, -6),
        (211, -6),
        (212, -6),
        (213, -6),
        (214, -6),
        (215, -6),
        (216, -6),
        (217, -6),
        (218, -6),
        (219, -6),
        (220, -6),
        # Section Macker
        # (253, 8),
        # (254, 8),
        # (265, 15),
        # (266, 15),
        # (250, 13),
        # (251, 13),
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
        (35, -10),
        (140, -10),
        (195, 13),
        (280, 20),
    ],
    "powerup_locations": [
        {"x": 50, "y": 5, "type": 3},
        {"x": 182, "y": -7, "type": 3},
        {"x": 83, "y": 3, "type": 2},
        {"x": 108, "y": 5, "type": 0},
    ],
    "enemy_locations": [
        # {
        #     "x": 40,
        #     "y": 7,
        #     "image": "enemies/trance-totem.png",
        #     "speed": 1,
        #     "patrol_range": 20,
        #     "size_multiplier": 4,
        #     "health": 15,
        #     "damage": 5,
        #     "shoot_range": 0,
        #     "chase_range": 10,
        #     "melee_damage": 2,
        #     "can_throw_explosives": False,
        #     "can_summon_minions": False,  # ← Add this line to enable minion spawning
        # },
        {
            "x": 130,
            "y": 6,
            "image": "enemies/trance-totem.png",
            "speed": 2,
            "patrol_range": 100,
            "size_multiplier": 4,
            "health": 15,
            "damage": 5,
            "shoot_range": 5,
            "chase_range": 10,
            "melee_damage": 2,
            "can_throw_explosives": False,
        },
        {
            "x": 170,
            "y": -5,
            "image": "enemies/trance-jesus.png",
            "speed": 3,
            "patrol_range": 100,
            "size_multiplier": 4,
            "health": 20,
            "damage": 5,
            "shoot_range": 30,
            "chase_range": 20,
            "melee_damage": 4,
            "can_throw_explosives": False,
        },
        {
            "x": 215,
            "y": -12,
            "image": "enemies/trance-hippie.png",
            "speed": 1,
            "patrol_range": 30,
            "size_multiplier": 4,
            "health": 20,
            "damage": 2,
            "shoot_range": 30,
            "chase_range": 5,
            "melee_damage": 2,
        },
        {
            "x": 255,
            "y": 20,
            "image": "enemies/trance-okf.png",
            "speed": 2,
            "patrol_range": 300,
            "size_multiplier": 4,
            "health": 40,
            "damage": 5,
            "shoot_range": 0,
            "chase_range": 100,
            "melee_damage": 15,
            "can_throw_explosives": False,
        },
    ],
    # Extended trophy locations - more collectibles
    "weapon_locations": [
        {"x": 170, "y": -20, "type": "wasserpistole"},  # Erste Waffe
    ],
    # Moving platform locations - new feature!
    "moving_platform_locations": [
        {
            "x": 138,  # Starting x position (grid units)
            "y": -10,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 8,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 142,  # Starting x position (grid units)
            "y": -7,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 8,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 164,  # Starting x position (grid units)
            "y": -12,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 8,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 170,
            "y": -14,
            "platform_type": "block",
            "movement_type": "circular",
            "speed": 30,
            "distance": 5,  # This acts as radius for circular movement
            "direction": "horizontal",  # Not used for circular
        },
        {
            "x": 258,  # Starting x position (grid units)
            "y": 15,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 3,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 254,  # Starting x position (grid units)
            "y": 17,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 3,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 247,  # Starting x position (grid units)
            "y": 14,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 242,  # Starting x position (grid units)
            "y": 16,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 4,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 281,  # Starting x position (grid units)
            "y": 10,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 2,  # Movement speed (pixels per frame)
            "distance": 10,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 263,  # Starting x position (grid units)
            "y": -12,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 29,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 258,  # Starting x position (grid units)
            "y": -9,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 257,  # Starting x position (grid units)
            "y": -9,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 256,  # Starting x position (grid units)
            "y": -19,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 10,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
    ],
    "trophy_locations": [
        (84, 0),
        (133, -2),
        (256, -20),
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

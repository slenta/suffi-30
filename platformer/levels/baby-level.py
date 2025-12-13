level_config = {
    "x_bounds": [-100, 8000],  # Extended for underground tunnel and surface climb
    "y_bounds": [-200, 500],
    "level_time": 360,  # 6 minutes for the longer level
    # Player spawn point
    "player_start": (205, 13),
    # Ground platforms with gaps to jump over
    "grass_locations": [
        # Starting area - safe zone
        *[(i, 14) for i in range(-5, 24)],
        *[(i, 14) for i in range(28, 43)],
        *[(i, 14) for i in range(49, 65)],
        *[(i, 26) for i in range(101, 130)],
        *[(i, 22) for i in range(135, 160)],
        *[(i, 14) for i in range(101, 125)],
        *[(i, 14) for i in range(130, 160)],
        *[(i, 14) for i in range(165, 200)],
        # Ascent from tunnel (climbing up)
        *[(i, 22) for i in range(350, 400)],
        # Final surface section
        *[(i, 14) for i in range(420, 460)],
    ],
    "block_locations": [
        # Original blocks
        (8, 13),
        (9, 13),
        (10, 12),
        (11, 12),
        (12, 11),
        (13, 11),
        (14, 10),
        (15, 10),
        (16, 9),
        (17, 9),
        (51, 13),
        (52, 13),
        (53, 12),
        (54, 12),
        (55, 11),
        (56, 11),
        (57, 10),
        (58, 10),
        (60, 8),
        (61, 8),
        (62, 8),
        (63, 8),
        (64, 8),
        (70, 5),
        (71, 5),
        (72, 5),
        (73, 5),
        (74, 2),
        (80, 2),
        (81, 2),
        (82, 2),
        (83, 2),
        (84, 2),
        (88, 12),
        (89, 12),
        (90, 24),
        (91, 24),
        (92, 24),
        (93, 24),
        (140, 12),
        (142, 12),
        (144, 12),
        (160, 18),
        (161, 18),
        (167, 12),
        (168, 12),
        (195, 12),
        (196, 12),
        (180, 10),
        (181, 10),
        (182, 10),
        # === NEW: Underground Tunnel Blocks ===
        # Tunnel entrance decorations
        (200, 13),
        (201, 13),
        (202, 12),
        (203, 11),
        *[(205, i) for i in range(14, 19)],
        *[(205, i) for i in range(22, 24)],
        *[(202, i) for i in range(19, 28)],
        # Underground ceiling blocks (simulate cave roof)
        *[(i, 24) for i in range(205, 295)],
        *[(i, 28) for i in range(202, 214)],
        *[(i, 28) for i in range(218, 239)],
        *[(i, 28) for i in range(243, 254)],
        *[(i, 28) for i in range(258, 300)],
        *[(i, 31) for i in range(214, 218)],
        *[(i, 31) for i in range(239, 243)],
        *[(i, 31) for i in range(254, 258)],
        # After tunnel platforms
        *[(i, 8) for i in range(355, 360)],
        *[(i, 5) for i in range(362, 368)],
        *[(i, 1) for i in range(365, 368)],
        *[(i, -2) for i in range(355, 360)],
        *[(i, -6) for i in range(350, 355)],
        *[(i, -10) for i in range(343, 348)],
        *[(i, -14) for i in range(335, 341)],
        # Final area platforms
        (423, 12),
        (422, 12),
        (450, 12),
        (451, 12),
    ],
    "moving_platform_locations": [
        {
            "x": 353,
            "y": 10,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 10,
            "direction": "vertical",
        },
        {
            "x": 301,
            "y": 30,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 12,
            "direction": "horizontal",
        },
        {
            "x": 302,
            "y": 30,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 12,
            "direction": "horizontal",
        },
        {
            "x": 311,
            "y": 28,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 15,
            "direction": "horizontal",
        },
        {
            "x": 312,
            "y": 28,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 15,
            "direction": "horizontal",
        },
        {
            "x": 322,
            "y": 26,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 13,
            "direction": "horizontal",
        },
        {
            "x": 323,
            "y": 26,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 13,
            "direction": "horizontal",
        },
        {
            "x": 332,
            "y": 24,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 15,
            "direction": "horizontal",
        },
        {
            "x": 333,
            "y": 24,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 15,
            "direction": "horizontal",
        },
        {
            "x": 403,
            "y": 16,
            "platform_type": "block",
            "movement_type": "circular",
            "speed": 1,
            "distance": 3,
        },
        {
            "x": 410,
            "y": 12,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 10,
        },
        {
            "x": 411,
            "y": 12,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 10,
        },
    ],
    "spike_locations": [
        {"x": 214, "y": 30, "direction": "up", "damage": 20},
        {"x": 217, "y": 30, "direction": "up", "damage": 20},
        {"x": 239, "y": 30, "direction": "up", "damage": 20},
        {"x": 242, "y": 30, "direction": "up", "damage": 20},
        {"x": 257, "y": 30, "direction": "up", "damage": 20},
    ],
    # Gems
    "gem_locations": [
        (17, 8),
        (60, 12),
        (120, 12),
        (202, 18),
        (310, 23),  # In tunnel
        (342, 19),  # On mid platform
    ],
    # Power-Ups
    "powerup_locations": [
        {"x": 22, "y": 12, "type": 4},  # Babybrei after tutorial
        {"x": 130, "y": 10, "type": 4},  # Babybrei before boss
        # === NEW: Underground powerups ===
        {"x": 280, "y": 23, "type": 4},  # Babybrei in tunnel
        {"x": 470, "y": 13, "type": 4},  # Babybrei near surface exit
    ],
    # Weapons
    "weapon_locations": [
        {"x": 12, "y": 10, "type": "milchflasche"},  # Erste Waffe (on stairs)
    ],
    # Enemies (using centralized config templates)
    "enemy_locations": [
        {"type": "baby_erzieherin", "x": 174, "y": 11},  # Boss in arena center
        {"type": "teddybear", "x": 140, "y": 20},  # Mini-boss
        {"type": "teddybear", "x": 230, "y": 23},  # Tunnel entrance guard
        {"type": "buchstabe", "x": 250, "y": 23},  # Tunnel entrance guard
        {"type": "buchstabe", "x": 210, "y": 23},  # Tunnel entrance guard
        {"type": "teddybear", "x": 360, "y": 21},  # After gap
        {"type": "buchstabe", "x": 337, "y": -15},  # Top of platforms
        {
            "type": "baby_erzieherin",
            "x": 430,
            "y": 11,
            "size_multiplier": 4,
        },  # Final boss before exit
    ],
    # Trophies (3 total - placed as milestones)
    "trophy_locations": [
        (40, 13),
        (90, 13),
        (135, 13),
        (255, 29),  # Tunnel milestone
        (390, 21),  # Deep tunnel milestone
        (336, -15),  # Deep tunnel milestone
    ],
    "trophy_image": "trophy.png",
    "exit_location": (455, 13),  # Final exit on surface
    "checkpoint_locations": [
        {"x": 200, "y": 10},  # Checkpoint nach Notaufnahme
        {"x": 350, "y": 22},  # Checkpoint nach der Sprungpassage
    ],
    # Assets
    "background_music": "assets/music/babyshark.ogg",
    "background_image": "assets/backgrounds/kindergarten-bg.png",
    "background_scroll_speed": 0.2,
    "player_image": "player/baby-suffi-left.png",
}

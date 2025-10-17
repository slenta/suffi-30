level_config = {
    "x_bounds": [-300, 9000],  # Extended gameworld width (doubled)
    "y_bounds": [-400, 400],  # Increased gameworld height for more vertical space
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
        # pyramid structure
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
        (79, 3),
        (80, 3),
        (81, 3),
        (82, 3),
        (83, 3),
        (84, 3),
        # höhle für powerup type 2
        (82, 11),
        (83, 11),
        (84, 11),
        (85, 11),
        (86, 11),
        (89, 12),
        (89, 13),
        (89, 11),
        (89, 10),
        (89, 9),
        (89, 8),
        (88, 8),
        (87, 8),
        (86, 8),
        (85, 8),
        (84, 8),
        (83, 8),
        (82, 8),
        (82, 9),
        (82, 10),
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
        (175, 6),
        (175, 7),
        (175, 8),
        # Trphy
        (168, 12),
        (169, 7),
        (170, 2),
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
        {"x": 83, "y": 10, "type": 2},
        {"x": 108, "y": 5, "type": 0},
    ],
    "enemy_locations": [
        # Original enemies
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
        {"x": 50, "y": 13, "type": "wasserpistole"},  # Erste Waffe
    ],
    "trophy_locations": [
        # Original trophies
        (84, 2),
        (175, 1),
    ],
    "trophy_image": "data/images/mushroom.png",  # Path to trophy image for UI display
    # Extended exit location - much further
    "exit_location": (420, 13),
    "background_music": "music/level1.mp3",  # Path relative to game root, or use absolute path
    # "background_image": "backgrounds/level2.png",  # Path to background image
    "background_scroll_speed": 0.2,  # Slower parallax for advanced level
    # Alternative backgrounds for type 2 power-up
    "alternative_backgrounds": [
        "backgrounds/level2.png",  # You can add more background images here to cycle through
    ],
    # Alternative music tracks for type 2 power-up
    "alternative_music_tracks": [
        "music/level2.mp3",  # Plays when switching to first alternative background
    ],
}

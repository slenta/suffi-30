level_config = {
    "x_bounds": [-600, 3000],  # Gameworld width
    "y_bounds": [-200, 300],  # Gameworld height
    # "level_time": 180,  # Time limit in seconds (3 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    "player_spawn": (0, -10),  # Example: spawn at grid position (5, 1)
    "grass_locations": [(i, 0) for i in range(0, 10)]
    + [(i, -20) for i in range(40, 60)]
    + [(i, -16) for i in range(65, 80)]
    + [(i, -8) for i in range(90, 100)]
    + [(i, -12) for i in range(112, 120)]
    + [(i, -4) for i in range(115, 140)]
    + [(i, 0) for i in range(145, 150)],
    "block_locations": [
        (10, -1),
        (11, -2),
        (12, -3),
        (13, -4),
        (14, -5),
        (15, -6),
        (16, -6),
        (17, -6),
        (18, -6),
        (19, -6),
        (20, -6),
        (23, -9),
        (24, -10),
        (25, -11),
        (26, -12),
        (27, -12),
        (28, -12),
        (29, -12),
        (30, -12),
        (31, -12),
        (34, -15),
        (35, -16),
        (38, -18),
        (39, -19),
        (61, -10),
        (62, -10),
        (63, -10),
        (80, 0),
        (81, 0),
        (82, 0),
        (83, 0),
        (84, 0),
        (85, 0),
        (86, 0),
        (87, 0),
        (88, 0),
        (89, 0),
        (137, -18),
        (138, -18),
        (139, -16),
        (140, -14),
    ],
    "poppable_block_locations": [
        (142, -21),  # Disappears after being popped
        # Dict format allows specifying type and item
        {
            "x": 142,
            "y": -25,
            "type": "item",
            "item": {"type": "gem", "image": "gem.png"},
        },  # Releases a gem
        {
            "x": 73,
            "y": -19,
            "type": "item",
            "item": {"type": "powerup", "powerup_type": 3},
        },
        {
            "x": 96,
            "y": -12,
            "type": "item",
            "item": {"type": "powerup", "powerup_type": 5},
        },
        {
            "x": 48,
            "y": -24,
            "type": "item",
            "item": {"type": "powerup", "powerup_type": 3},
        },
        {
            "x": 6,
            "y": -4,
            "type": "item",
            "item": {"type": "powerup", "powerup_type": 5},
        },
    ],
    "gem_locations": [(15, -8), (142, -17)],
    "powerup_locations": [
        {"x": 35, "y": -19, "type": 3},  # pulver
        {"x": 85, "y": -2, "type": 5},  # punisher
        {"x": 61, "y": -15, "type": 5},
        {"x": 78, "y": -20, "type": 0},
    ],
    # Enemy locations (using centralized config with overrides)
    "enemy_locations": [
        {"type": "trance_shroom", "x": 18, "y": -8},
        {"type": "trance_shroom", "x": 29, "y": -14},
        {"type": "trance_shroom", "x": 55, "y": -25},
        {"type": "druide", "x": 130, "y": -7},
    ],
    "trophy_locations": [(63, -12), (115, -16)],
    "ladder_locations": [
        (60, -20),
        (60, -19),
        (60, -18),
        (60, -17),
        (60, -16),
        (60, -15),
        (60, -14),
        (60, -13),
        (60, -12),
        (60, -11),
        (60, -10),
        (80, -16),
        (80, -15),
        (80, -14),
        (80, -13),
        (80, -12),
        (80, -11),
        (80, -10),
        (80, -9),
        (80, -8),
        (80, -7),
        (80, -6),
        (80, -5),
        (80, -4),
        (80, -3),
        (80, -2),
        (80, -1),
        (89, -1),
        (89, -2),
        (89, -3),
        (89, -4),
        (89, -5),
        (89, -6),
        (89, -7),
        (89, -8),
    ],
    "trophy_image": "trophy.png",  # Path to trophy image (relative to assets/images)
    # Moving platform locations
    "moving_platform_locations": [
        {
            "x": 98,
            "y": -12,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 10,
            "direction": "horizontal",
        },
        {
            "x": 103,
            "y": -15,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 10,
            "direction": "horizontal",
        },
        {
            "x": 142,  # Starting x position (grid units)
            "y": -16,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 15,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
    ],
    "trophy_image": "mushroom.png",
    "exit_location": (148, -1),
    "spike_locations": [],
    # "background_music": "assets/music/level1.ogg",  # Path relative to game root
    # "background_image": "assets/backgrounds/level1_bg.png",  # Path to background image
    "background_scroll_speed": 1,  # Optional: parallax scrolling speed (0.0 = static, 1.0 = moves with camera)
    # Use same alternative backgrounds as parent level to maintain consistency
    "alternative_backgrounds": [
        "assets/backgrounds/trancefloor.png",
    ],
    "alternative_music_tracks": [
        "assets/music/trancefloor.ogg",
    ],
}

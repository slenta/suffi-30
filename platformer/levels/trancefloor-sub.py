level_config = {
    "x_bounds": [-600, 3000],  # Gameworld width
    "y_bounds": [-200, 300],  # Gameworld height
    # "level_time": 180,  # Time limit in seconds (3 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    "player_spawn": (0, -10),  # Example: spawn at grid position (5, 1)
    "grass_locations": [(i, 0) for i in range(0, 10)]
    + [(i, -20) for i in range(29, 60)]
    + [(i, -16) for i in range(65, 80)]
    + [(i, -8) for i in range(90, 120)]
    + [(i, -4) for i in range(125, 140)]
    + [(i, 0) for i in range(145, 150)],
    "block_locations": [
        (10, -1),
        (11, -2),
        (12, -3),
        (13, -4),
        (14, -5),
        (15, -6),
        # (16, -7),
        # (17, -8),
        (18, -9),
        (19, -10),
        (20, -11),
        (21, -12),
        # (22, -13),
        # (23, -14),
        (24, -15),
        (25, -16),
        # (26, -17),
        # (27, -18),
        (28, -19),
        (29, -20),
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
    ],
    "gem_locations": [
        (15, -8),
    ],
    "powerup_locations": [
        # {"x": 15, "y": -8, "type": 3},
        {"x": 85, "y": -2, "type": 3},
        {"x": 61, "y": -15, "type": 5},
    ],
    # Enemy locations (using centralized config with overrides)
    "enemy_locations": [
        {"type": "trance_shroom", "x": 35, "y": -25},
        {"type": "trance_shroom", "x": 45, "y": -25},
        {"type": "trance_shroom", "x": 55, "y": -25},
        {"type": "druide", "x": 100, "y": -12},
    ],
    "trophy_locations": [(63, -12), (135, -7)],
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
    "moving_platform_locations": [],
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

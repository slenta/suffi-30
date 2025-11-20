level_config = {
    "x_bounds": [-600, 3000],  # Gameworld width
    "y_bounds": [-200, 300],  # Gameworld height
    "level_time": 180,  # Time limit in seconds (3 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    "player_spawn": (0, 10),  # Example: spawn at grid position (5, 1)
    "grass_locations": [(i, 14) for i in range(-20, 20)]
    + [(i, 14) for i in range(23, 51)],
    "block_locations": [
        (18, 4),
        (19, 4),
    ],
    "gem_locations": [(10, 13), (11, 13)],
    "powerup_locations": [],
    # Enemy locations (using centralized config with overrides)
    "enemy_locations": [
        {"type": "druide", "x": 40, "y": -5},
    ],
    "trophy_locations": [(10, 10)],
    "trophy_image": "trophy.png",  # Path to trophy image (relative to assets/images)
    # Moving platform locations
    "moving_platform_locations": [],
    "exit_location": (50, 13),
    "spike_locations": [],
    "background_music": "assets/music/level1.ogg",  # Path relative to game root
    "background_image": "assets/backgrounds/level1_bg.png",  # Path to background image
    "background_scroll_speed": 1,  # Optional: parallax scrolling speed (0.0 = static, 1.0 = moves with camera)
}

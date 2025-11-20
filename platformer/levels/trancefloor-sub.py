level_config = {
    "x_bounds": [-600, 3000],  # Gameworld width
    "y_bounds": [-200, 300],  # Gameworld height
    # "level_time": 180,  # Time limit in seconds (3 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    "player_spawn": (20, -10),  # Example: spawn at grid position (5, 1)
    "grass_locations": [(i, 0) for i in range(0, 75)]
    + [(i, 0) for i in range(80, 150)],
    "block_locations": [
        (50, -24),
    ],
    "gem_locations": [],
    "powerup_locations": [],
    # Enemy locations (using centralized config with overrides)
    "enemy_locations": [
        {"type": "presslufthanna", "x": 120, "y": -5},
    ],
    "trophy_locations": [(50, -25)],
    "trophy_image": "trophy.png",  # Path to trophy image (relative to assets/images)
    # Moving platform locations
    "moving_platform_locations": [],
    "exit_location": (148, -1),
    "spike_locations": [],
    # "background_music": "assets/music/level1.ogg",  # Path relative to game root
    # "background_image": "assets/backgrounds/level1_bg.png",  # Path to background image
    "background_scroll_speed": 1,  # Optional: parallax scrolling speed (0.0 = static, 1.0 = moves with camera)
}

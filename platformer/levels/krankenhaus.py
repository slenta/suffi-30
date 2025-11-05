level_config = {
    "x_bounds": [-600, 3000],  # Gameworld width
    "y_bounds": [-200, 300],  # Gameworld height
    "level_time": 180,  # Time limit in seconds (3 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    # "player_spawn": (5, 1),  # Example: spawn at grid position (5, 1)
    "grass_locations": [(i, 14) for i in range(-20, 20)]
    + [(i, 14) for i in range(25, 40)]
    + [(i, 40) for i in range(35, 70)]
    + [(i, 40) for i in range(75, 100)]
    + [(i, 40) for i in range(105, 300)],
    "block_locations": [
        (18, 4),
        (19, 4),
    ],
    "gem_locations": [(10, 13), (11, 13)],
    "powerup_locations": [
        {"x": 40, "y": 10, "type": 0},  # Power-up to make the player bigger
        {"x": 60, "y": 8, "type": 1},  # Power-up to make the player faster
    ],
    # Enemy locations (using centralized config with overrides)
    "enemy_locations": [
        {
            "type": "trump",
            "x": 200,
            "y": 38,
            "speed": 2,
            "patrol_range": 100,
            "size_multiplier": 2,
            "health": 7,
            "damage": 14,
            "shoot_range": 14,
            "melee_damage": 5,
        },
    ],
    "trophy_locations": [(10, 5)],
    "trophy_image": "trophy.png",  # Path to trophy image (relative to assets/images)
    # Moving platform locations
    "moving_platform_locations": [
        {
            "x": 50,  # Starting x position (grid units)
            "y": 8,  # Starting y position (grid units)
            "platform_type": "grass",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 8,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 70,
            "y": 6,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1.5,
            "distance": 6,
            "direction": "vertical",
        },
    ],
    "exit_location": (300, 39),
    "spike_locations": [
        {"x": 0, "y": 9, "direction": "down", "damage": 10},
        {"x": 1, "y": 9, "direction": "down", "damage": 10},
    ],
    "background_music": "assets/music/level1.ogg",  # Path relative to game root
    "background_image": "assets/backgrounds/level1_bg.png",  # Path to background image
    "background_scroll_speed": 0.3,  # Optional: parallax scrolling speed (0.0 = static, 1.0 = moves with camera)
}

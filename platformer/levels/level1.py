level_config = {
    "x_bounds": [-600, 3000],  # Gameworld width
    "y_bounds": [-200, 300],  # Gameworld height
    "level_time": 180,  # Time limit in seconds (3 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    # "player_spawn": (5, 1),  # Example: spawn at grid position (5, 1)
    "grass_locations": [(i, 14) for i in range(-20, 20)]
    + [(i, 14) for i in range(25, 59)]
    + [(i, 14) for i in range(70, 120)],  # Flattened list of tuples
    "block_locations": [
        (18, 4),
        (19, 4),
        (20, 4),
        (21, 4),
        (11, 7),
        (12, 7),
        (13, 7),
        (14, 7),
        (25, 13),
        (25, 7),
        (26, 7),
        (27, 7),
        (17, 10),
        (18, 10),
        (19, 10),
        (38, 12),
        (38, 13),
        (45, 10),
        (46, 10),
        (47, 10),
        (61, 10),
        (63, 8),
        (65, 6),
        (79, 10),
        (80, 10),
        (81, 10),
    ],
    "gem_locations": [(20, 3), (12, 6), (26, 6), (36, 13), (65, 5)],
    "powerup_locations": [
        {"x": 40, "y": 10, "type": 0},  # Power-up to make the player bigger
        {"x": 60, "y": 8, "type": 1},  # Power-up to make the player faster
    ],
    "enemy_locations": [
        {
            "x": 30,
            "y": 12,
            "image": "trump.png",
            "speed": 2,
            "patrol_range": 100,
            "size_multiplier": 2,
            "health": 7,
            "damage": 14,  # Damage dealt by bullets
            "shoot_range": 14,  # Shooting range in tiles
            "chase_range": 10,  # Chasing range in tiles
            "melee_damage": 5,  # Melee damage
        },
        {
            "x": 80,
            "y": 10,
            "image": "elon.png",
            "speed": 3,
            "patrol_range": 150,
            "size_multiplier": 4,
            "health": 15,
            "damage": 25,
            "shoot_range": 20,
            "chase_range": 15,
            "melee_damage": 10,
        },
        {
            "x": 200,
            "y": 10,
            "image": "police.png",
            "speed": 5,
            "patrol_range": 150,
            "size_multiplier": 3,
            "health": 15,
            "damage": 50,
            "shoot_range": 20,
            "chase_range": 15,
            "melee_damage": 10,
        },
    ],
    "trophy_locations": [(10, 5), (26, 6), (80, 8)],
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
    "exit_location": (95, 13),
    "spike_locations": [
        {"x": 10, "y": 13, "direction": "up", "damage": 10},
        {"x": 11, "y": 13, "direction": "up", "damage": 10},
        {"x": 0, "y": 9, "direction": "down", "damage": 10},
        {"x": 1, "y": 9, "direction": "down", "damage": 10},
    ],
    "background_music": "assets/music/level1.ogg",  # Path relative to game root
    "background_image": "assets/backgrounds/level1_bg.png",  # Path to background image
    "background_scroll_speed": 0.3,  # Optional: parallax scrolling speed (0.0 = static, 1.0 = moves with camera)
}

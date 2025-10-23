"""
Sub-level: Underground Cave
This is an example sub-level accessed via a pipe from the main level.
"""

level_config = {
    "x_bounds": [-300, 2000],  # Smaller sub-level
    "y_bounds": [-200, 300],
    # Player spawn point - where player appears when entering this sub-level
    "player_spawn": (5, 1),
    # Floor grass locations
    "grass_locations": [(i, 14) for i in range(-20, 80)],
    # Block locations - create a small cave-like structure
    "block_locations": [
        # Upper ceiling
        (10, 3),
        (11, 3),
        (12, 3),
        (13, 3),
        (14, 3),
        (20, 4),
        (21, 4),
        (22, 4),
        (30, 5),
        (31, 5),
        (32, 5),
        (33, 5),
        # Mid-level platforms
        (15, 10),
        (16, 10),
        (17, 10),
        (25, 8),
        (26, 8),
        (27, 8),
        (35, 11),
        (36, 11),
        # Small obstacles
        (40, 13),
        (41, 13),
        (50, 12),
        (51, 12),
        (52, 12),
    ],
    # Gem locations - rewards for exploring the sub-level
    "gem_locations": [
        (12, 2),
        (21, 3),
        (31, 4),
        (16, 9),
        (26, 7),
        (51, 11),
    ],
    # Powerup locations
    "powerup_locations": [
        {"x": 60, "y": 10, "type": 0},  # Size power-up
    ],
    # Enemy locations - make it challenging
    "enemy_locations": [
        {
            "x": 25,
            "y": 13,
            "image": "trump.png",
            "speed": 1,
            "patrol_range": 50,
            "size_multiplier": 1,
            "health": 2,
            "damage": 1,
            "shoot_range": 0,
        },
        {
            "x": 50,
            "y": 13,
            "image": "trump.png",
            "speed": 2,
            "patrol_range": 80,
            "size_multiplier": 1,
            "health": 3,
            "damage": 1,
            "shoot_range": 0,
        },
    ],
    # Weapon locations
    "weapon_locations": [],
    # Moving platform locations
    "moving_platform_locations": [
        {
            "x": 45,
            "y": 9,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 5,
            "direction": "horizontal",
        },
    ],
    # Trophy locations - collect trophy to open exit
    "trophy_locations": [
        (65, 10),
    ],
    "trophy_image": "trophy.png",
    # Exit location - completing this returns to main level
    "exit_location": (70, 13),
    # Optional: Different background for sub-level
    # "background_image": "assets/backgrounds/cave.png",
    "background_scroll_speed": 0.1,
    # No pipes in the sub-level (to keep it simple)
    "pipe_locations": [],
}

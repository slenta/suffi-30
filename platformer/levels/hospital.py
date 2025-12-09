level_config = {
    "x_bounds": [-500, 3000],  # Gameworld width
    "y_bounds": [-200, 300],  # Gameworld height
    "level_time": 240,  # Time limit in seconds (4 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    "player_spawn": (0, 10),  # Example: spawn at grid position (5, 1)
    # Extended grass platforms with challenging gaps
    "grass_locations": [(i, 14) for i in range(-20, 20)]
    + [(i, 14) for i in range(23, 35)]
    + [(i, 14) for i in range(40, 50)]
    + [(i, 14) for i in range(55, 70)]
    + [(i, 8) for i in range(72, 85)]
    + [(i, 14) for i in range(90, 110)]
    + [(i, 14) for i in range(115, 130)],
    # Challenging block structures throughout the level
    "block_locations": [
        # Starting pyramid structure
        (18, 13),
        (19, 12),
        (20, 11),
        (21, 10),
        (22, 9),
        (23, 8),
        (24, 9),
        (25, 10),
        (26, 11),
        (27, 12),
        (28, 13),
        # First gap - floating platforms
        *[(i, 10) for i in range(30, 33)],
        (35, 8),
        (36, 8),
        (37, 8),
        # Vertical tower challenge
        *[(42, i) for i in range(13, 7, -1)],
        (43, 7),
        (44, 7),
        (45, 7),
        *[(46, i) for i in range(7, 14)],
        # Staircase up
        (52, 13),
        (53, 12),
        (54, 11),
        (55, 10),
        (56, 9),
        (57, 8),
        (58, 7),
        # Hidden cave for powerup
        *[(i, 10) for i in range(60, 68)],
        *[(60, i) for i in range(10, 13)],
        *[(67, i) for i in range(10, 13)],
        # Staircase down to lower platform
        (70, 9),
        (71, 10),
        (72, 11),
        # Tower platforms on lower level
        *[(75, i) for i in range(8, 5, -1)],
        *[(78, i) for i in range(8, 4, -1)],
        *[(81, i) for i in range(8, 3, -1)],
        # Bridge back to main level
        *[(i, 10) for i in range(83, 88)],
        (87, 11),
        (88, 12),
        (89, 13),
        # Challenging zigzag section
        (92, 12),
        (93, 11),
        (94, 10),
        (95, 9),
        (96, 8),
        (97, 7),
        (98, 8),
        (99, 9),
        (100, 10),
        (101, 11),
        (102, 12),
        # Final tower before exit
        *[(105, i) for i in range(13, 8, -1)],
        *[(i, 8) for i in range(105, 110)],
        *[(110, i) for i in range(8, 14)],
        # Final platform gauntlet
        (112, 12),
        (113, 11),
        (115, 10),
        (117, 9),
        (119, 10),
        (121, 11),
        (123, 12),
        (125, 13),
    ],
    # Strategic gem placements
    "gem_locations": [
        (21, 7),  # Top of first pyramid
        (37, 6),  # After first gap
        (63, 8),  # Inside hidden cave
        (81, 1),  # Top of tallest tower
        (97, 5),  # Peak of zigzag
        (105, 7),  # Final tower
    ],
    # Powerups at key locations
    "powerup_locations": [
        {"x": 35, "y": 7, "type": 0},  # Speed boost before gap
        {"x": 63, "y": 9, "type": 2},  # Invincibility in cave
        {"x": 75, "y": 4, "type": 1},  # Jump boost on tower
        {"x": 100, "y": 8, "type": 3},  # Health near zigzag peak
    ],
    # Enemy locations (using centralized config with overrides)
    "enemy_locations": [
        {"type": "patient_follower", "x": 2, "y": 13},
        {"type": "patient", "x": 48, "y": 13},
        {"type": "patient", "x": 65, "y": 13},
        {"type": "patient", "x": 78, "y": 7},
        {"type": "patient", "x": 95, "y": 13},
        {"type": "patient", "x": 110, "y": 13},
        {"type": "patient", "x": 120, "y": 13},
    ],
    # Trophy checkpoints
    "trophy_locations": [
        (43, 6),  # After first tower
        (85, 9),  # After lower level section
        (110, 7),  # Final tower
    ],
    "trophy_image": "trophy.png",  # Path to trophy image (relative to assets/images)
    # Moving platforms for dynamic challenge
    "moving_platform_locations": [
        {
            "x": 38,
            "y": 10,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 5,
            "direction": "horizontal",
        },
        {
            "x": 50,
            "y": 11,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 4,
            "direction": "vertical",
        },
        {
            "x": 73,
            "y": 12,
            "platform_type": "block",
            "movement_type": "circular",
            "speed": 20,
            "distance": 3,
            "direction": "horizontal",
        },
        {
            "x": 107,
            "y": 10,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 6,
            "direction": "vertical",
        },
    ],
    # Ladder for vertical navigation
    "ladder_locations": [(85, i) for i in range(8, 14)],
    "exit_location": (128, 13),
    "spike_locations": [
        # Add danger zones
        *[
            {"x": i, "y": 15, "direction": "up", "damage": 10} for i in range(36, 39)
        ],  # Below first gap
        *[
            {"x": i, "y": 15, "direction": "up", "damage": 10} for i in range(51, 55)
        ],  # Below staircase
        *[
            {"x": i, "y": 15, "direction": "up", "damage": 10} for i in range(91, 104)
        ],  # Below zigzag section
    ],
    "background_music": "assets/music/level1.ogg",  # Path relative to game root
    "background_image": "assets/backgrounds/hospital_background_seamless.png",
    "background_scroll_speed": 0.3,  # Optional: parallax scrolling speed (0.0 = static, 1.0 = moves with camera)
    "block_image": "block_white_2.png",  # Custom block image for this level
}

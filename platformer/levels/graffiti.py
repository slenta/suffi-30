"""
Example level demonstrating the pipe/sub-level mechanic.

This level shows how to create pipes that lead to sub-levels,
similar to the green pipes in Mario games.
"""

level_config = {
    "x_bounds": [-600, 3000],
    "y_bounds": [-200, 300],
    # Basic floor
    "grass_locations": [(i, 14) for i in range(-20, 100)],
    # Some platforms and blocks
    "block_locations": [
        (20, 10),
        (21, 10),
        (22, 10),
        (40, 12),
        (41, 12),
        (60, 8),
        (61, 8),
        (62, 8),
    ],
    # A few gems
    "gem_locations": [
        (21, 9),
        (61, 7),
    ],
    # No powerups for simplicity
    "powerup_locations": [],
    # A simple enemy
    "enemy_locations": [
        # {
        #     "x": 50,
        #     "y": 13,
        #     "image": "trump.png",
        #     "speed": 1,
        #     "patrol_range": 100,
        #     "size_multiplier": 1,
        #     "health": 2,
        #     "damage": 1,
        #     "shoot_range": 0,
        # },
    ],
    # No weapons
    "weapon_locations": [],
    # No moving platforms
    "moving_platform_locations": [],
    # Trophy to collect
    "trophy_locations": [
        (45, 12),
    ],
    "trophy_image": "trophy.png",
    # Exit at the end
    "exit_location": (50, 13),
    # Pipe configuration - this is the important part!
    "pipe_locations": [
        {
            "x": 30,  # X position in grid units (where the pipe appears)
            "y": 13,  # Y position in pixels (usually on the ground: grid_y * 32)
            "sub_level": "sub-graffiti-yard",  # Name of the sub-level file (without .py extension)
            "return_x": 32,  # Where player spawns when returning (grid units)
            "return_y": 13,  # Y position when returning (grid units)
            "direction": "down",  # Direction to press: "down", "up", "left", or "right"
        },
        # You can add multiple pipes to different sub-levels:
        # {
        #     "x": 70,
        #     "y": 13 * 32,
        #     "sub_level": "sub-underwater",
        #     "return_x": 72,
        #     "return_y": 13,
        #     "direction": "down"
        # },
    ],
}

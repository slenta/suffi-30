"""
Example level demonstrating the pipe/sub-level mechanic.

This level shows how to create pipes that lead to sub-levels,
similar to the green pipes in Mario games.
"""

level_config = {
    "x_bounds": [-600, 3000],
    "y_bounds": [-200, 300],
    "level_time": 240,  # Time limit in seconds (4 minutes)
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
    # Poppable blocks (like Mario question blocks)
    "poppable_block_locations": [
        # Simple tuple format uses default "disappear" type
        (25, 9),  # Disappears after being popped
        # Dict format allows specifying type and item
        {"x": 26, "y": 9, "type": "fix"},  # Turns into solid block after popping
        {
            "x": 27,
            "y": 9,
            "type": "item",
            "item": {"type": "gem", "image": "gem.png"},
        },  # Releases a gem
        {
            "x": 45,
            "y": 10,
            "type": "item",
            "item": {"type": "powerup", "powerup_type": 1},
        },  # Releases a powerup
        {"x": 46, "y": 10, "type": "disappear"},  # Explicitly set to disappear
        {"x": 65, "y": 6, "type": "fix"},  # Another one that turns solid
    ],
    # A few gems
    "gem_locations": [
        (21, 9),
        (61, 7),
    ],
    # Powerups - place a flight powerup next to the pipe for testing
    "powerup_locations": [
        {"x": 29, "y": 11, "type": 6},
    ],
    # A simple enemy
    "enemy_locations": [
        {"type": "tightill", "x": 121, "y": -24},
        {"type": "robodog", "x": 70, "y": -24},
        {"type": "drone", "x": 120, "y": -24},
    ],
    # Weapon(s) placed near the pipe for testing — spraydose placed just above the pipe
    "weapon_locations": [
        {"x": 30, "y": 11, "type": "spraydose"},
    ],
    # No moving platforms
    "moving_platform_locations": [],
    # Add waterfall
    "waterfall_locations": [
        (9, y) for y in range(4, 14)
    ],  # 10 blocks high starting at y=4
    # Trophy to collect (using centralized config)
    "trophy_locations": [
        {"type": "standard", "x": 45, "y": 12},
    ],
    # Ladder locations
    "ladder_locations": [
        (5, 14),  # Bottom of ladder
        (5, 13),
        (5, 12),
        (5, 11),
        (5, 10),
        (5, 9),
        (5, 8),
        (5, 7),
        (5, 6),
        (5, 5),
        (5, 4),  # Top of ladder
    ],
    # No exit here — the sub-level exit will finish the whole level
    # Pipe configuration - this is the important part!
    "pipe_locations": [
        {
            "x": 30,  # X position in grid units (where the pipe appears)
            "y": 12,  # Y position in grid units (top of the pipe - pipe is 2 units tall, so bottom will be at y=14)
            "sub_level": "graffiti-sub",  # Name of the sub-level file (without .py extension)
            "return_x": 32,  # Where player spawns when returning (grid units)
            "return_y": 13,  # Y position when returning (grid units)
            "direction": "down",  # Direction to press: "down", "up", "left", or "right"
        },
        # You can add multiple pipes to different sub-levels:
        # {
        #     "x": 70,
        #     "y": 13 * 32,
        #     "sub_level": "underwater-sub",
        #     "return_x": 72,
        #     "return_y": 13,
        #     "direction": "down"
        # },
    ],
    "exit_location": (330, 11),
}

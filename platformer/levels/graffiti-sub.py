"""
Sub-level: Underground Cave
This is an example sub-level accessed via a pipe from the main level.
"""

level_config = {
    # Extended to the left to give more room for exploration
    # Increase left bound so player can move at least to x = -100 (grid units)
    # Cut level at x = -100 (grid units). Left side removed.
    # ground_start is in pixels so convert: -100 * GRIDSIZE (GRIDSIZE=18) = -1800
    "x_bounds": [-1800, 2000],
    "y_bounds": [-500, 300],
    # Player spawn point - where player appears when entering this sub-level
    "player_spawn": (5, 1),
    # Floor grass locations
    # Expand floor to the left so the player can move farther left
    # Floor grass: start at x = -94 so that x = -100..-95 has no grass
    "grass_locations": [(i, 14) for i in range(-94, 80)],
    # Use a different grass tile for this sublevel (placed in assets/images)
    "grass_image": "asche.png",
    # Block locations - create a small cave-like structure
    "block_locations": [
        # Left Wall
        (4,-2),
        (3,-2),
        
        (3,3),
        (3,4),
        (3,5),
        (3,7),
        (3,8),
        (3,9),
        (3,10),
        (3,11),
        (3,12),
        (3,13),
        # left to the wall
        #top stairs
        (2,-2),
        (1,-2),
        (0,-2),
        (-1,-1),
        (-2,0),
        (-3,1),
        # Exit blocks
        (-6, 6),
        (-6, 5),
        (-6, 4),
        (-7, 3),
        (-8, 3),
        (-6,3),
        # obere begrenzung tunnel
    *[(i, 7) for i in range(-7, -76, -1)],
    *[(i, 6) for i in range(-7, -76, -1)],
        # left top stairs 
        (-9,3),
        (-10,2),
        (-11,1),
        (-12,0),
        (-13,-1),
        (-14,-2),
        (-15,-3),
        (-16,-4),
        (-17,-5),
        (-18,-6),
        #lower left tunnel
    *[(i, 11) for i in range(0, -80, -1)],   
    *[(i, 10) for i in range(0, -80, -1)],
        # leftest wall
    *[(-87, i) for i in range(13, -100, -1)], 
    *[(-80, i) for i in range(9, -20, -1)],
        # right to the wall
        # Upper ceiling
        (13, 3),
        (14, 3),
        (20, 4),
        (21, 4),
        (22, 4),
        # Mid-level platforms
        (15, 10),
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
        (33, -3),
    ],
    # Powerup locations
    "powerup_locations": [
        {"x": 60, "y": 10, "type": 0},  # Size power-up (existing)
        {"x": 15, "y": 9, "type": 1},   # Speed power-up above mid platform (reachable)
        {"x": 25, "y": 7, "type": 2},   # Background changer above moving platforms
        {"x": 55, "y": 3, "type": 3},   # Chaos power-up near circular platform (use moving platform to reach)
        {"x": -84, "y": 13, "type": 7},  # a joint to safe you
    ],
    # Enemy locations - make it challenging
    "enemy_locations": [
        {
            "x": 25,
            "y": 13,
            "type": "tightill",
            "speed": 2,
            "patrol_range": 50,
            "size_multiplier": 3,
            "health": 50,
            "damage": 2,
            "shoot_range": 30,
            "range": 4,
            "reload_time": 3,
        },
        {
            "x": 50,
            "y": 13,
            "type": "robodog",
            "speed": 3,
            "patrol_range": 80,
            "size_multiplier": 3,
            "health": 15,
            "damage": 1,
            "shoot_range": 0,
        }, {
            "x": -32,
            "y": 13,
            "type": "robodog",
            "speed": 3,
            "patrol_range": 80,
            "size_multiplier": 2,
            "health": 15,
            "damage": 1,
            "shoot_range": 0,
        },
        {
            "x": -2,
            "y": 5,
            "type": "drone",
            "speed": 4,
            "patrol_range": 100,
            "size_multiplier": 3,
            "health": 10,
            "damage": 1,
            "shoot_range": 4,
        },
    ],
    # Weapon locations
    "weapon_locations": [
        # placed at x=17 so it's reachable from the central platforms
        {"x": 17, "y": 9, "type": "spraydose"},
    ],
    # Moving platform locations
    "moving_platform_locations": [
        {
            "x": 36,
            "y": 9,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 10,
            "direction": "horizontal",
        },
        {
            "x": 55,
            "y": 4,
            "platform_type": "block",
            "movement_type": "circular",
            "speed": 1,
            "distance": 4,
        },
        {
            "x": 33,
            "y": 1,
            "platform_type": "block",
            "movement_type": "circular",
            "speed": 1,
            "distance": 4,

        },
    ],
    # Ladder locations - group ladders as separate lists so each stack gets its own LadderTop
    "ladder_locations": [
        # Main ladder near the center (bottom -> top)
        [
            (2, 13),
            (2, 12),
            (2, 11),
            (2, 10),
            (2, 9),
            (2, 8),
            (2, 7),
            (2, 6),
            (2, 5),
            (2, 4),
            (2, 3),
        ],
        # Left ladder near x = -86 (bottom -> top)
        [
            (-86, 13),
            (-86, 12),
            (-86, 11),
            (-86, 10),
            (-86, 9),
            (-86, 8),
            (-86, 7),
            (-86, 6),
            (-86, 5),
            (-86, 4),
            (-86, 3),
            (-86, 2),
        ],
        # Developer-added ladder at x = -82 from y = -4 down to y = -11 (bottom -> top: -4 ... -11)
        [
            (-81, -4),
            (-81, -5),
            (-81, -6),
            (-81, -7),
            (-81, -8),
            (-81, -9),
            (-81, -10),
            (-81, -11),
        ],
    ],
    # Trophy locations - collect trophy to open exit
    "trophy_locations": [
        (65, 10),
        (-82, -50)
    ],
    "trophy_image": "trophy.png",
    # If True, always reset collected/killed tracking when this level is loaded.
    # Useful during development so placed enemies/items reappear each load.
    "reset_killed_on_load": True,
    # Exit location - completing this returns to main level
    "exit_location": (-7, 5),
    # If True, when this sub-level's exit is reached the whole level is finished
    # instead of returning to the parent level. Useful when the sub-level contains
    # the final door for the complete stage.
    "finish_parent_on_exit": True,
    # Optional: Different background for sub-level
    "background_image": "assets/backgrounds/graffiti_sublevel.png",
    "background_scroll_speed": 0.1,
    # Level-specific block look: dusty brown/grey tint (R,G,B)
    "block_tint": (120, 110, 100),
    # Invisible poppable block: stays pass-through until hit from below
    "poppable_block_locations": [
        {"x": 4, "y": 10, "type": "disappear"},
        {"x":7, "y": 4, "type": "invisible"},
        {"x":4, "y": 6, "type": "invisible"},
        {"x":-82, "y": -49, "type": "invisible"},
        {"x":-83, "y": -49, "type": "invisible"},
        {"x":-85, "y": -10, "type": "invisible"},
        {"x":16, "y": 10, "type": "powerup", "powerup_type": 1},
        # invisible blöcke für zugang zu ziel
        {"x":-77, "y": 6, "type": "invisible"},
        {"x":-78, "y": 6, "type": "invisible"},
        {"x":-79, "y": 6, "type": "invisible"},
        {"x":-80, "y": 6, "type": "invisible"},

        # Development: a poppable block that spawns a power-up type 7 (joint)
        # The block stays solid after being popped.
        {
            "x": -85,
            "y": -16,
            "type": "item",
            "item": {"type": "powerup", "powerup_type": 7},
        },
    ],
    # No pipes in the sub-level (to keep it simple)
    "pipe_locations": [],
}

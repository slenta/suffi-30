"""
Sub-level: Underground Cave
This is an example sub-level accessed via a pipe from the main level.
"""

level_config = {
    # Extended to the left to give more room for exploration
    # Increase left bound so player can move at least to x = -100 (grid units)
    "x_bounds": [-2000, 2000],  # Extended left boundary (pixels)
    "y_bounds": [-200, 300],
    # Player spawn point - where player appears when entering this sub-level
    "player_spawn": (5, 1),
    # Floor grass locations
    # Expand floor to the left so the player can move farther left
    "grass_locations": [(i, 14) for i in range(-500, 80)],
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
        (-7, 4),
        (-8, 4),
        (-6,3),
        (-7,7),
        (-8,7),
        (-9,7),
        (-10,7),
        (-11,7),
        (-12,7),
        # left top stairs 
        (-9,3),
        (-10,2),
        (-11,1),
        (-12,0),
        #lower left tunnel
        (0,10),
        ( -1,10),
        ( -2,10),
        ( -3,10),
        ( -4,10),
        ( -5,10),
        (-6,10),
        (-7,10),
        (-8,10),
        (-9,10),
        (-10,10),
        (-11,10),
        (-12,10),
        (-13,10),
        (-14,10),
        (-15,10),
        (-16,10),
        (-17,10),
        (-18,10),
        (-19,10),
        (-20,10),
        (-21,10),
        (-22,10),
        (-23,10),
        (-24,10),
        (-25,10),
        (-26,10),
        (-27,10),
        (-28,10),
        (-29,10),
        (-30,10),
        (-31,10),
        (-32,10),
        (-33,10),
        (-34,10),
        (-35,10),
        (-36,10),
        (-37,10),
        (-38,10),
        (-39,10),
        (-40,10),
        (-41,10),
        (-42,10),
        (-43,10),
        (-44,10),
        (-45,10),
        (-46,10),
        (-47,10),
        (-48,10),
        (-49,10),
        (-50,10),
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
        (33, -3)
    ],
    # Powerup locations
    "powerup_locations": [
        {"x": 60, "y": 10, "type": 0},  # Size power-up (existing)
        {"x": 15, "y": 9, "type": 1},   # Speed power-up above mid platform (reachable)
        {"x": 25, "y": 7, "type": 2},   # Background changer above moving platforms
        {"x": 55, "y": 3, "type": 3},   # Chaos power-up near circular platform (use moving platform to reach)
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
    # Ladder locations
    "ladder_locations": [
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
    # Trophy locations - collect trophy to open exit
    "trophy_locations": [
        (65, 10),
    ],
    "trophy_image": "trophy.png",
    # Exit location - completing this returns to main level
    "exit_location": (-7, 6),
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
        {"x":16, "y": 10, "type": "powerup", "powerup_type": 1},
    ],
    # No pipes in the sub-level (to keep it simple)
    "pipe_locations": [],
}

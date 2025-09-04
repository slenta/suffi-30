level_config = {
    "x_bounds": [-600, 6000],  # Extended gameworld width (doubled)
    "y_bounds": [-400, 400],  # Increased gameworld height for more vertical space
    
    # Extended grass locations - keeping original and adding more sections
    "grass_locations": [(i, 14) for i in range(-20, 20)]
    + [(i, 14) for i in range(25, 59)]
    + [(i, 14) for i in range(70, 120)]
    + [(i, 14) for i in range(130, 170)]  # New section 1
    + [(i, 14) for i in range(180, 220)]  # New section 2
    + [(i, 14) for i in range(240, 280)]  # New section 3
    + [(i, 14) for i in range(300, 350)]  # New section 4
    + [(i, 14) for i in range(370, 420)],  # Final section
    
    # Extended block locations - original plus new challenging platforming sections
    "block_locations": [
        # Original blocks
        (18, 4), (19, 4), (20, 4), (21, 4),
        (11, 7), (12, 7), (13, 7), (14, 7),
        (25, 13), (25, 7), (26, 7), (27, 7),
        (17, 10), (18, 10), (19, 10),
        (38, 12), (38, 13),
        (45, 10), (46, 10), (47, 10),
        (61, 10), (63, 8), (65, 6),
        (79, 10), (80, 10), (81, 10),
        
        # New challenging platform sections
        # Section 1 - Vertical tower
        (125, 13), (125, 12), (125, 11), (125, 10), (125, 9),
        (127, 8), (129, 7), (131, 6),
        
        # Section 2 - Staircase up
        (140, 13), (142, 12), (144, 11), (146, 10), (148, 9), (150, 8),
        
        # Section 3 - Floating platforms
        (160, 11), (162, 11), (164, 9), (166, 9), (168, 7),
        
        # Section 4 - Underground maze entrance
        (185, 13), (185, 12), (187, 11), (189, 10), (191, 9),
        (195, 13), (196, 13), (197, 13), (198, 13),
        
        # Section 5 - High platforms
        (210, 8), (212, 8), (214, 6), (216, 6), (218, 4),
        
        # Section 6 - Complex structure
        (250, 13), (251, 13), (252, 13),
        (250, 10), (252, 10),
        (251, 7), (253, 7), (255, 7),
        (254, 4), (256, 4),
        
        # Section 7 - Moving platform bases
        (270, 12), (272, 10), (274, 8), (276, 6),
        
        # Section 8 - Pyramid structure
        (320, 13), (321, 13), (322, 13), (323, 13), (324, 13),
        (321, 10), (322, 10), (323, 10),
        (322, 7),
        
        # Section 9 - Final challenge platforms
        (380, 11), (382, 9), (384, 7), (386, 5), (388, 3),
        (395, 13), (396, 13), (397, 13), (398, 13),
        
        # Section 10 - Boss area platforms
        (410, 10), (412, 10), (414, 10), (416, 10),
    ],
    
    # Extended gem locations - more rewards throughout the longer level
    "gem_locations": [
        # Original gems
        (20, 3), (12, 6), (26, 6), (36, 13), (65, 5),
        
        # New gems in extended sections
        (131, 5),    # Top of tower
        (150, 7),    # End of staircase
        (168, 6),    # High floating platform
        (198, 12),   # Maze entrance
        (218, 3),    # Highest platform
        (256, 3),    # Top of complex structure
        (276, 5),    # Moving platform area
        (322, 6),    # Pyramid top
        (388, 2),    # Final challenge peak
        (415, 9),    # Boss area
    ],
    
    # Extended powerup locations - more strategic power-ups
    "powerup_locations": [
        # Original powerups
        {"x": 40, "y": 10, "type": 0},   # Power-up to make the player bigger
        {"x": 60, "y": 8, "type": 1},   # Power-up to make the player faster
        
        # New strategic powerups
        {"x": 150, "y": 7, "type": 0},  # Size boost before difficult section
        {"x": 220, "y": 5, "type": 1},  # Speed boost for precision jumps
        {"x": 280, "y": 7, "type": 0},  # Size boost for enemy encounters
        {"x": 350, "y": 12, "type": 1}, # Speed boost for final challenges
        {"x": 390, "y": 4, "type": 0},  # Final size boost before boss
    ],
    
    # Extended enemy locations - progressively more challenging
    "enemy_locations": [
        # Original enemies
        {
            "x": 30, "y": 12, "image": "trump.png", "speed": 2,
            "patrol_range": 100, "size_multiplier": 2, "health": 7,
            "damage": 14, "shoot_range": 14, "chase_range": 10, "melee_damage": 5,
        },
        {
            "x": 80, "y": 10, "image": "elon.png", "speed": 3,
            "patrol_range": 150, "size_multiplier": 4, "health": 15,
            "damage": 25, "shoot_range": 20, "chase_range": 15, "melee_damage": 10,
        },
        {
            "x": 200, "y": 10, "image": "police.png", "speed": 5,
            "patrol_range": 150, "size_multiplier": 1, "health": 15,
            "damage": 50, "shoot_range": 20, "chase_range": 15, "melee_damage": 10,
        },
        
        # New enemies with increasing difficulty
        {
            "x": 155, "y": 10, "image": "trump.png", "speed": 3,
            "patrol_range": 120, "size_multiplier": 2.5, "health": 10,
            "damage": 18, "shoot_range": 16, "chase_range": 12, "melee_damage": 7,
        },
        {
            "x": 230, "y": 13, "image": "elon.png", "speed": 4,
            "patrol_range": 180, "size_multiplier": 3, "health": 20,
            "damage": 30, "shoot_range": 22, "chase_range": 18, "melee_damage": 12,
        },
        {
            "x": 285, "y": 11, "image": "police.png", "speed": 6,
            "patrol_range": 200, "size_multiplier": 1.5, "health": 25,
            "damage": 60, "shoot_range": 25, "chase_range": 20, "melee_damage": 15,
        },
        {
            "x": 340, "y": 12, "image": "trump.png", "speed": 4,
            "patrol_range": 150, "size_multiplier": 3, "health": 15,
            "damage": 25, "shoot_range": 18, "chase_range": 15, "melee_damage": 10,
        },
        {
            "x": 375, "y": 10, "image": "elon.png", "speed": 5,
            "patrol_range": 220, "size_multiplier": 4.5, "health": 30,
            "damage": 40, "shoot_range": 28, "chase_range": 25, "melee_damage": 18,
        },
        # Boss enemy
        {
            "x": 415, "y": 9, "image": "police.png", "speed": 7,
            "patrol_range": 250, "size_multiplier": 2, "health": 50,
            "damage": 80, "shoot_range": 30, "chase_range": 25, "melee_damage": 25,
        },
    ],
    
    # Extended trophy locations - more collectibles
    "trophy_locations": [
        # Original trophies
        (10, 5), (26, 6), (80, 8),
        
        # New trophies in extended sections
        (145, 11),   # Staircase area
        (170, 6),    # Floating platforms
        (255, 6),    # Complex structure
        (325, 12),   # Pyramid base
        (390, 12),   # Final area
    ],
    
    # Extended exit location - much further
    "exit_location": (420, 13),
}

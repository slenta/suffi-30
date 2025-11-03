level_config = {
    "x_bounds": [-100, 5000],  # Much longer level
    "y_bounds": [-200, 500],
    "level_time": 240,  # 4 minutes for exploration
    # Player spawn point
    "player_start": (2, 13),
    # Ground platforms with gaps to jump over
    "grass_locations": [
        # Starting area - safe zone
        *[(i, 14) for i in range(-5, 24)],
        *[(i, 14) for i in range(28, 43)],
        *[(i, 14) for i in range(49, 65)],
        *[(i, 26) for i in range(101, 130)],
        *[(i, 22) for i in range(135, 160)],
        *[(i, 14) for i in range(101, 125)],
        *[(i, 14) for i in range(130, 160)],
        *[(i, 14) for i in range(165, 200)],
    ],
    "block_locations": [
        (8, 13),
        (9, 13),
        (10, 12),
        (11, 12),
        (12, 11),
        (13, 11),
        (14, 10),
        (15, 10),
        (16, 9),
        (17, 9),
        (51, 13),
        (52, 13),
        (53, 12),
        (54, 12),
        (55, 11),
        (56, 11),
        (57, 10),
        (58, 10),
        (60, 8),
        (61, 8),
        (62, 8),
        (63, 8),
        (64, 8),
        (70, 5),
        (71, 5),
        (72, 5),
        (73, 5),
        (74, 2),
        (80, 2),
        (81, 2),
        (82, 2),
        (83, 2),
        (84, 2),
        (88, 12),
        (89, 12),
        (90, 24),
        (91, 24),
        (92, 24),
        (93, 24),
        (140, 12),
        (142, 12),
        (144, 12),
        (160, 18),
        (161, 18),
        (167, 12),
        (168, 12),
        (195, 12),
        (196, 12),
        (180, 10),
        (181, 10),
        (182, 10),
    ],
    # Gems
    "gem_locations": [
        (17, 8),
        (60, 12),
        (120, 12),
    ],
    # Power-Ups
    "powerup_locations": [
        {"x": 22, "y": 12, "type": 4},  # Babybrei after tutorial
        {"x": 130, "y": 10, "type": 4},  # Babybrei before boss
    ],
    # Weapons
    "weapon_locations": [
        {"x": 12, "y": 10, "type": "milchflasche"},  # Erste Waffe (on stairs)
    ],
    # Enemies
    "enemy_locations": [
        {
            "x": 180,
            "y": 13,
            "image": "enemies/baby-erzieherin.png",  # Boss in arena center
            "speed": 1,
            "patrol_range": 150,
            "size_multiplier": 4,
            "health": 50,
            "damage": 5,
            "shoot_range": 0,  # Nur Melee
            "chase_range": 10,
            "melee_damage": 10,
            "can_throw_explosives": False,
        },
        {
            "x": 140,
            "y": 20,
            "image": "enemies/teddybear.png",
            "speed": 1,
            "patrol_range": 50,
            "size_multiplier": 3,
            "health": 30,
            "damage": 5,
            "shoot_range": 0,  # Nur Melee
            "chase_range": 10,
            "melee_damage": 10,
            "can_throw_explosives": False,
        },
    ],
    # Trophies (3 total - placed as milestones)
    "trophy_locations": [
        (40, 13),
        (90, 13),
        (135, 13),
    ],
    "trophy_image": "trophy.png",
    # Exit (behind boss)
    "exit_location": (190, 13),
    # Assets
    "background_music": "assets/music/kindergarten_bg.ogg",
    "background_image": "assets/backgrounds/kindergarten_bg.png",
    "background_scroll_speed": 0.2,
}

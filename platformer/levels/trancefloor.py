level_config = {
    "x_bounds": [-300, 9000],  # Extended gameworld width (doubled)
    "y_bounds": [-1230, 1170],  # Increased gameworld height for more vertical space
    "level_time": 300,  # Time limit in seconds (5 minutes)
    # "player_spawn": (285, 12),
    "player_spawn": (210, -35),
    # Extended grass locations - keeping original and adding more sections
    "grass_locations": [(i, -16) for i in range(-20, 16)]
    + [(i, -16) for i in range(25, 30)]
    + [(i, -16) for i in range(40, 59)]
    + [(i, -16) for i in range(78, 99)]
    + [(i, -22) for i in range(112, 150)]
    + [(i, -32) for i in range(150, 175)]
    + [(i, -32) for i in range(180, 190)]
    + [(i, -32) for i in range(193, 203)]
    + [(i, -32) for i in range(206, 218)]
    + [(i, -16) for i in range(225, 240)]
    + [(240, i) for i in range(-16, -8)]
    + [(i, -8) for i in range(240, 285)]
    + [(270, i) for i in range(-16, -10)]
    + [(i, -16) for i in range(270, 281)]
    + [(i, -16) for i in range(282, 290)]
    + [(i, -40) for i in range(290, 420)]
    + [(i, -20) for i in range(420, 500)],
    # Extended block locations - original plus new challenging platforming sections
    "block_locations": [
        # pyramid structure
        (15, -17),
        (16, -18),
        (17, -19),
        (18, -20),
        (19, -21),
        (20, -22),
        (21, -21),
        (22, -20),
        (23, -19),
        (24, -18),
        (25, -17),
        # abgrund
        *[(i, -20) for i in range(33, 36)],
        # first gem
        *[(i, -20) for i in range(45, 47)],
        *[(i, -23) for i in range(49, 51)],
        (43, -27),
        (42, -27),
        *[(i, -32) for i in range(47, 50)],
        *[(i, -35) for i in range(54, 56)],
        *[(i, -39) for i in range(40, 49)],
        # 2. abgrund
        *[(i, -20) for i in range(60, 62)],
        *[(i, -24) for i in range(64, 66)],
        (68, -28),
        (69, -27),
        (70, -26),
        (71, -25),
        (72, -24),
        (73, -23),
        (74, -22),
        (75, -21),
        # first trophy
        *[(i, -29) for i in range(77, 85)],
        # höhle für powerup type 2
        *[(i, -19) for i in range(82, 87)],
        # (89, 12),
        # (89, 13),
        *[(89, i) for i in range(-22, -18)],
        *[(i, -22) for i in range(85, 89)],
        *[(i, -29) for i in range(85, 96)],
        # (84, 8),
        # (83, 8),
        *[(82, i) for i in range(-25, -19)],
        *[(i, -25) for i in range(82, 90)],
        (92, -22),
        # Towers Abgrund
        *[(103, i) for i in range(-20, -16)],
        *[(108, i) for i in range(-20, -16)],
        # Next gem
        (136, -31),
        (134, -30),
        (132, -29),
        (130, -28),
        (128, -27),
        # First Weapon
        *[(i, -44) for i in range(159, 162)],
        # Hippie Enemy
        *[(i, -36) for i in range(210, 221)],
        # Section Leiter
        *[(i, -49) for i in range(338, 345)],
        (337, -47),
        (336, -44),
        (336, -42),
        (336, -41),
        *[(i, -27) for i in range(290, 297)],
        *[(i, -27) for i in range(300, 301)],
        *[(i, -27) for i in range(304, 305)],
        *[(i, -27) for i in range(308, 309)],
        *[(i, -27) for i in range(312, 313)],
    ],
    # Extended gem locations - more rewards throughout the longer level
    "gem_locations": [
        # Original gems
        (35, -40),
        (140, -40),
        (195, -17),
        (280, -10),
        (311, -32),
    ],
    "ladder_locations": [(289, i) for i in range(-40, -16)],
    "powerup_locations": [
        {"x": 50, "y": -25, "type": 3},
        {"x": 182, "y": -37, "type": 3},
        {"x": 83, "y": -27, "type": 2},
        {"x": 108, "y": -25, "type": 0},
    ],
    # Enemies (using centralized config templates with overrides where needed)
    "enemy_locations": [
        {"type": "trance_totem", "x": 130, "y": -24},
        {"type": "trance_jesus", "x": 170, "y": -35},
        {"type": "trance_hippie", "x": 215, "y": -42},
        {"type": "trance_okf", "x": 255, "y": -10},
        # DJ Booth boss with custom shoot_cooldown
        {
            "type": "dj_booth",
            "x": 336,
            "y": -55,
            "shoot_cooldown": 20,
            "melee_damage": 100,
        },
        # Special final enemy (yourself!) - custom config needed
        {
            "x": 480,
            "y": -22,
            "image": "player/suffi.png",
            "speed": 3,
            "patrol_range": 300,
            "size_multiplier": 6,
            "health": 200,
            "damage": 10,
            "shoot_range": 100,
            "chase_range": 400,
            "melee_damage": 15,
            "can_throw_explosives": False,
            "encounter_message": "The final enemy on the trancefloor – it is yourself!",
        },
    ],
    # Extended trophy locations - more collectibles
    "weapon_locations": [
        {"x": 170, "y": -50, "type": "wasserpistole"},  # Erste Waffe
    ],
    # Moving platform locations - new feature!
    "moving_platform_locations": [
        {
            "x": 138,  # Starting x position (grid units)
            "y": -40,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 8,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 142,  # Starting x position (grid units)
            "y": -37,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 8,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 164,  # Starting x position (grid units)
            "y": -42,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 8,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 170,
            "y": -44,
            "platform_type": "block",
            "movement_type": "circular",
            "speed": 30,
            "distance": 5,  # This acts as radius for circular movement
            "direction": "horizontal",  # Not used for circular
        },
        {
            "x": 258,  # Starting x position (grid units)
            "y": -15,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 3,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 254,  # Starting x position (grid units)
            "y": -13,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 3,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 247,  # Starting x position (grid units)
            "y": -16,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 242,  # Starting x position (grid units)
            "y": -14,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 4,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 281,  # Starting x position (grid units)
            "y": -20,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 2,  # Movement speed (pixels per frame)
            "distance": 10,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 263,  # Starting x position (grid units)
            "y": -42,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 29,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 258,  # Starting x position (grid units)
            "y": -39,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 257,  # Starting x position (grid units)
            "y": -39,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 256,  # Starting x position (grid units)
            "y": -49,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 1,  # Movement speed (pixels per frame)
            "distance": 10,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "vertical",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 320,  # Starting x position (grid units)
            "y": -49,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 2,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 327,  # Starting x position (grid units)
            "y": -49,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 2,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 315,  # Starting x position (grid units)
            "y": -45,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 2,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
        {
            "x": 322,  # Starting x position (grid units)
            "y": -45,  # Starting y position (grid units)
            "platform_type": "block",  # "grass" or "block"
            "movement_type": "linear",  # "linear" or "circular"
            "speed": 2,  # Movement speed (pixels per frame)
            "distance": 5,  # Distance to travel (grid units for linear, radius for circular)
            "direction": "horizontal",  # "horizontal" or "vertical" (for linear only)
        },
    ],
    "trophy_locations": [
        (84, -30),
        (133, -32),
        (256, -50),
    ],
    "trophy_image": "mushroom.png",
    "exit_location": (499, -22),
    # Pipe configuration - this is the important part!
    "pipe_locations": [
        {
            "x": 219,  # X position in grid units (where the pipe appears)
            "y": -38,  # Y position in grid units (top of the pipe - pipe is 2 units tall, so bottom will be at y=14)
            "sub_level": "trancefloor-sub",  # Name of the sub-level file (without .py extension)
            "return_x": 219,  # Where player spawns when returning (grid units)
            "return_y": -38,  # Y position when returning (grid units)
            "direction": "down",  # Direction to press: "down", "up", "left", or "right"
        },
    ],
    "background_music": "assets/music/default.ogg",
    # "background_image": "assets/backgrounds/trancefloor.png",
    "background_scroll_speed": 1,
    "alternative_backgrounds": [
        "assets/backgrounds/trancefloor.png",
    ],
    "alternative_music_tracks": [
        "assets/music/trancefloor.ogg",
    ],
}

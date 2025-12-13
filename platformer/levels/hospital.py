level_config = {
    "x_bounds": [-1000, 10000],  # Gameworld width
    "y_bounds": [-500, 800],  # Gameworld height
    "level_time": 480,  # Time limit in seconds (8 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    "player_spawn": (100, 8),  # Example: spawn at grid position (5, 1)
    # Player thought bubble at level start
    "player_start_message": "Nur noch diese Schicht \n und dann endlich zur Fusion...",
    "player_start_message_color": (255, 255, 255),  # White
    # Custom player image for this level (placed in assets/images/)
    "player_image": "player/suffi_aerztin.png",  # Change to your custom player image
    # Total trophies including dropped items (overrides automatic counting)
    "total_trophies": 3,  # 3 in trophy_locations
    "required_items_for_exit": ["busticket"],  # List of required item IDs
    # Timeout Message (customize for this level)
    "timeout_message": "",
    # Game over Messaage (customize for this level)
    "game_over_message": "Du hast es nicht zum Bus geschafft!",
    "game_over_message_color": (255, 0, 0),  # z.B. Rot
    # Use a different grass tile for this sublevel (placed in assets/images)
    "grass_image": "krankenhaus_boden.png",
    # Extended grass platforms with challenging gaps
    "grass_locations": [(i, 14) for i in range(-40, -23)]
    + [(i, 14) for i in range(-20, 16)]
    + [(i, 14) for i in range(55, 70)]
    + [(i, 8) for i in range(76, 90)]
    + [(i, 14) for i in range(100, 120)]
    + [(i, 14) for i in range(115, 165)]
    + [(i, 14) for i in range(206, 220)]  # Gap for jumping puzzle starts at 220
    + [(i, 14) for i in range(268, 420)]
    + [(i, 25) for i in range(200, 268)],
    # Challenging block structures throughout the level
    "block_locations": [
        # Starting obstacle
        (18, 13),
        (21, 11),
        (24, 9),
        (30, 13),
        (33, 11),
        (39, 13),
        # Jumping puzzle
        (128, 9),
        (134, 5),
        (128, 1),
        (134, -3),
        (128, -7),
        (112, -11),
        # Way back after Trophy
        (88, 29),
        (85, 28),
        (82, 25),
        (79, 23),
        (78, 21),
        # Obstacle near end
        (167, 11),
        (172, 8),
        (177, 5),
        (182, 8),
        (187, 11),
        (192, 8),
        (197, 5),
        (202, 5),
        # Erste Treppe für Gegner
        (206, 5),
        (206, 6),
        (206, 7),
        (206, 8),
        (206, 9),
        (206, 10),
        (206, 11),
        (206, 12),
        (206, 13),
        (206, 14),
        (206, 15),
        # Zweite Treppe für Gegner
        (219, 15),
        (219, 14),
        (219, 13),
        (219, 12),
        (219, 11),
        (219, 10),
        (219, 9),
        (219, 8),
        (219, 7),
        (219, 6),
        (219, 5),
        # Weg zurück nach schwieriger Sprungpassage
        (190, 13),
        (191, 14),
        (192, 15),
        (193, 16),
        (194, 17),
        (195, 18),
        (196, 19),
        (197, 20),
        (198, 21),
        (199, 22),
        (200, 23),
        *[(i, 20) for i in range(40, 75)],
    ],
    # Poppable blocks (like Mario question blocks)
    "poppable_block_locations": [
        {
            "x": 50,
            "y": 5,
            "type": "item",
            "item": {"type": "powerup", "powerup_type": 3},
            "image": "medizinschrank.png",  # Eigenes Bild
        },  # Releases Pulver
        {
            "x": 82,
            "y": 17,
            "type": "item",
            "item": {"type": "powerup", "powerup_type": 3},
            "image": "medizinschrank.png",  # Eigenes Bild
        },  # Releases Pulver
        {"x": 218, "y": 9, "type": "invisible"},  # Invisible block
          {
            "x": 288,
            "y": 9,
            "type": "item",
            "item": {"type": "powerup", "powerup_type": 3},
            "image": "medizinschrank.png",  # Eigenes Bild
        },  # Releases Pulver
    ],
    # Strategic gem placements
    "gem_locations": [
        (21, 7),  # Top of starting obstacle
        (37, 6),  # After first gap
        (63, 8),  # Inside hidden cave
        (81, 1),  # Top of tallest tower
        (100, 4),  # Peak of zigzag
        (128, -9),  # Jumping puzzle
        (187,9), # Near end
        (278,9), # Vor House
    ],
    # Powerups at key locations
    "powerup_locations": [
        {"x": 128, "y": 4, "type": 6},  # Health in jumping puzzle
    ],
    # Enemy locations (using centralized config with overrides)
    "enemy_locations": [
        {
            "type": "doctor_f_follower",
            "x": 2,
            "y": 13,
            "encounter_message": "Frau Hegselmann, schön,\ndass sie so spontan einspringen konnten!",
            "encounter_message_color": (0, 255, 0),  # Green
        },
        {
            "type": "patient",
            "x": 56,
            "y": 13,
            "encounter_message": "Da sind sie ja endlich!",
            "encounter_message_color": (255, 0, 0),  # Red
        },
        {
            "type": "patient_f_young",
            "x": 65,
            "y": 13,
            "encounter_message": "Haben sie kurz Zeit für mich?",
            "encounter_message_color": (255, 0, 0),  # Red
        },
        {
            "type": "doctor_f_young",
            "x": 82,
            "y": 6,
            "encounter_message": "Frau Hegselmann, können Sie sich \n bitte kurz in der Notaufnahme melden?",
            "encounter_message_color": (255, 0, 0),  # Red
        },
        {
            "type": "doctor_old",
            "x": 120,
            "y": 13,
            "encounter_message": "Sie müssen mich vertreten, ich muss \n meinen Porsche in die Werkstatt bringen.",
            "encounter_message_color": (255, 0, 0),  # Red
        },
        {
            "type": "patient_f",
            "x": 140,
            "y": 13,
            "encounter_message": "Lassen Sie mich nicht allein \n das ist Altersdiskriminierung!",
            "encounter_message_color": (0, 255, 0),  # Green
        },
        {
            "type": "patient",
            "x": 150,
            "y": 13,
            "encounter_message": "Ich möchte den Chefarzt sprechen!",
            "encounter_message_color": (0, 255, 0),  # Green
        },
        {
            "type": "patient",
            "x": 160,
            "y": 13,
            "encounter_message": "Ich werde mich beschweren!",
            "encounter_message_color": (0, 255, 0),  # Green
        },
        {
            "type": "patient_f_young",
            "x": 212,
            "y": 13,
            "encounter_message": "Sie gehen erst, wenn ich geheilt bin!",
            "encounter_message_color": (0, 255, 0),  # Green
            "drop_on_death": {
                "type": "powerup",
                "powerup_type": 6,
            },
        },
        {
            "type": "jonas",
            "x": 270,
            "y": 13,
        },
        {
            "type": "paul",
            "x": 275,
            "y": 13,
        },
        {
            "type": "house",
            "x": 310,
            "y": 13,
            "encounter_message": "Sie wollen doch nicht etwa schon gehen? \n Ihre Schicht fängt doch gerade erst an!",
            "drop_on_death": {
                "type": "required_item",
                "item_id": "busticket",
                "image": "Ticket.png",
            },
        },
    ],
    "trophy_locations": [
        (43, -3),  # First jumping obstacle
        (91, 19),  # Bottom of ladder
        (112, -14),  # Jumping puzzle end
    ],
    "trophy_image": "AU.png",  # Path to trophy image (relative to assets/images)
    # Moving platforms for dynamic challenge
    "moving_platform_locations": [
        {
            "x": 43,
            "y": 10,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 5,
            "direction": "horizontal",
        },
        {
            "x": 40,
            "y": 2,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 7,
            "direction": "vertical",
        },
        {
            "x": 50,
            "y": 9,
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
            "speed": 2,
            "distance": 3,
            "direction": "horizontal",
        },
        {
            "x": 100,
            "y": 7,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 6,
            "direction": "vertical",
        },
        {
            "x": 116,
            "y": -7,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 6,
            "direction": "horizontal",
        },
        # Knifflige Sprungpassage (x: 220-280)
        # Start: Horizontal beweglicher Block
        {
            "x": 222,
            "y": 10,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 6,
            "direction": "horizontal",
        },
        # Vertikal beweglicher Block (muss Timing treffen)
        {
            "x": 232,
            "y": 8,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 7,
            "direction": "vertical",
        },
        # Schnell horizontal (schwieriges Timing)
        {
            "x": 236,
            "y": 10,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 5,
            "direction": "horizontal",
        },
        # Vertikal beweglicher Block (muss Timing treffen)
        {
            "x": 246,
            "y": 8,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 7,
            "direction": "vertical",
        },
        # Langsam vertikal (Ruhepunkt)
        {
            "x": 250,
            "y": 4,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 1,
            "distance": 5,
            "direction": "vertical",
        },
        # Kombiniert: Horizontal beweglich hoch oben
        {
            "x": 252,
            "y": 3,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 6,
            "direction": "horizontal",
        },
        # Letzter vertikal beweglicher Block zum Ziel
        {
            "x": 260,
            "y": 4,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 2,
            "distance": 8,
            "direction": "vertical",
        },
        # Finale Plattform (statisch als Ziel)
        {
            "x": 265,
            "y": 11,
            "platform_type": "block",
            "movement_type": "linear",
            "speed": 0,
            "distance": 0,
            "direction": "horizontal",
        },
    ],
    # Ladder for vertical navigation
    "ladder_locations": [(91, i) for i in range(8, 20)],
    "exit_location": (380, 12),
    "exit_closed_image": "Bus.png",  # Optional
    "exit_open_image": "Bus.png",  # Optional
    "exit_size_multiplier": 16,  # Make the bus 16 times bigger (default is 2)
    "spike_locations": [
        # Add danger
        *[
            {"x": i, "y": 12, "direction": "up", "damage": 50} for i in range(19, 21)
        ],  # in first obstacle
        *[
            {"x": i, "y": 10, "direction": "up", "damage": 50} for i in range(22, 24)
        ],  # in first obstacle
        *[
            {"x": i, "y": 11, "direction": "up", "damage": 50} for i in range(26, 29)
        ],  # in first obstacle
        *[
            {"x": i, "y": 11, "direction": "up", "damage": 50} for i in range(35, 38)
        ],  # in first obstacle
        *[
            {"x": i, "y": 15, "direction": "up", "damage": 10} for i in range(51, 55)
        ],  # Below staircase
        *[
            {"x": i, "y": 15, "direction": "up", "damage": 10} for i in range(91, 100)
        ],  # Below zigzag section
    ],
    # Pipe configuration - this is the important part!
    "pipe_locations": [
        {
            "x": 86,  # X position in grid units (where the pipe appears)
            "y": 6,  # Y position in grid units (top of the pipe - pipe is 2 units tall, so bottom will be at y=14)
            "sub_level": "hospital-sub",  # Name of the sub-level file (without .py extension)
            "return_x": 100,  # Where player spawns when returning (grid units)
            "return_y": 13,  # Y position when returning (grid units)
            "direction": "down",  # Direction to press: "down", "up", "left", or "right"
        },
    ],
    "checkpoint_locations": [
    {"x": 108, "y": 9},  # Checkpoint nach Notaufnahme
    {"x": 283, "y": 9},  # Checkpoint nach der Sprungpassage
],
    "background_music": "assets/music/greys.mp3",  # Path relative to game root
    "background_image": "assets/backgrounds/hospital_background_seamless.png",
    "background_scroll_speed": 0.3,  # Optional: parallax scrolling speed (0.0 = static, 1.0 = moves with camera)
    "block_image": "block_white_2.png",  # Custom block image for this level
}

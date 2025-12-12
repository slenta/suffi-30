level_config = {
    "x_bounds": [-1000, 10000],  # Gameworld width
    "y_bounds": [-500, 800],  # Gameworld height
    "level_time": 240,  # Time limit in seconds (4 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    "player_spawn": (150, 8),  # Example: spawn at grid position (5, 1)
    # Player thought bubble at level start
    "player_start_message": "Nur noch diese Schicht \n und dann endlich zur Fusion...",
    "player_start_message_color": (255, 255, 255),  # White
    # Custom player image for this level (placed in assets/images/)
    "player_image": "player/suffi_aerztin.png",  # Change to your custom player image
    # Total trophies including dropped items (overrides automatic counting)
    "total_trophies": 3,  # 3 in trophy_locations 
    "required_items_for_exit": ["busticket"],  # List of required item IDs
    # Use a different grass tile for this sublevel (placed in assets/images)
    "grass_image": "krankenhaus_boden.png",
    # Extended grass platforms with challenging gaps
    "grass_locations": [(i, 14) for i in range(-40, -23)]
    + [(i, 14) for i in range(-20, 16)]
    + [(i, 14) for i in range(55, 70)]
    + [(i, 8) for i in range(76, 90)]
    + [(i, 14) for i in range(100, 120)]
    + [(i, 14) for i in range(115, 400)],
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
        (88,29),
        (85,28),
        (82,25),
        (79,23),
        (78,21),
        *[(i, 20) for i in range(40, 75)]
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
    ],

    # Strategic gem placements
    "gem_locations": [
        (21, 7),  # Top of starting obstacle
        (37, 6),  # After first gap
        (63, 8),  # Inside hidden cave
        (81, 1),  # Top of tallest tower
        (97, 5),  # Peak of zigzag
        (128, -9),  # Jumping puzzle
    ],
    # Powerups at key locations
    "powerup_locations": [
        {"x": 10, "y": 7, "type": 0},  # Speed boost before gap
        {"x": 10, "y": 9, "type": 2},  # Invincibility in cave
        {"x": 10, "y": 4, "type": 1},  # Jump boost on tower
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
            "x": 83,
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
            "type": "patient_f_young",
            "x": 150,
            "y": 13,
            "encounter_message": "This hospital\nis cursed!",
            "encounter_message_color": (0, 255, 0),  # Green
        },
        {
            "type": "patient",
            "x": 160,
            "y": 13,
            "encounter_message": "Don't leave\nme here!",
            "encounter_message_color": (0, 255, 0),  # Green
        },
        {
            "type": "jonas",
            "x": 180,
            "y": 13,
        },
        {
            "type": "paul",
            "x": 185,
            "y": 13,
        },
        {
            "type": "house",
            "x": 200,
            "y": 13,
            "encounter_message": "Sie wollen doch nicht etwa schon gehen? \n Die Schicht fängt doch gerade erst an!",
            "drop_on_death": {
                "type": "required_item",
                "item_id": "busticket",
                "image": "Ticket.png"
            }
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
            "x": 99,
            "y": 10,
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
    ],
    # Ladder for vertical navigation
    "ladder_locations": [(91, i) for i in range(8, 20)],
    "exit_location": (330, 11),
    "exit_closed_image": "Bus.png", # Optional
    "exit_open_image": "Bus.png",   # Optional
    "exit_size_multiplier": 16,     # Make the bus 16 times bigger (default is 2)
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
    "background_music": "assets/music/greys.mp3",  # Path relative to game root
    "background_image": "assets/backgrounds/hospital_background_seamless.png",
    "background_scroll_speed": 0.3,  # Optional: parallax scrolling speed (0.0 = static, 1.0 = moves with camera)
    "block_image": "block_white_2.png",  # Custom block image for this level
}

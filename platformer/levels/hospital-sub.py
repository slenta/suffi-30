level_config = {
    "x_bounds": [-1000, 5000],  # Gameworld width
    "y_bounds": [-200, 300],  # Gameworld height
    "level_time": 240,  # Time limit in seconds (4 minutes)
    # Player spawn point (optional) - x and y coordinates in grid units
    # If not specified, defaults to PLAYER_START_X, PLAYER_START_Y from settings.py
    "player_spawn": (0, 8),  # Example: spawn at grid position (5, 1)
    # Player thought bubble at level start
    # Custom player image for this level (placed in assets/images/)
    "player_image": "player/suffi_aerztin.png",  # Change to your custom player image
    # Use a different grass tile for this sublevel (placed in assets/images)
    "grass_image": "krankenhaus_boden.png",
    # Extended grass platforms with challenging gaps
    "grass_locations": [(i, 14) for i in range(-40, -23)]
    + [(i, 14) for i in range(-23, 300)],
    # Block locations - floating platforms and structures
    "block_locations": [],
    "gem_locations": [],
    # Powerups at key locations
    "powerup_locations": [],
    "moving_platform_locations": [],
    "trophy_locations": [],
    # Enemy locations (using centralized config with overrides)
    "enemy_locations": [
        {
            "type": "patient_f_follower",
            "x": 2,
            "y": 13,
            "encounter_message": "Aua, mein Bein!",
            "encounter_message_color": (0, 255, 0),  # Green
        },
        {
            "type": "patient_follower",
            "x": 25,
            "y": 13,
        },
        {
            "type": "patient_f_young_follower",
            "x": 45,
            "y": 13,
        },
        {
            "type": "patient_follower",
            "x": 72,
            "y": 13,
            "encounter_message": "Warum dauert das hier so lange?",
            "encounter_message_color": (255, 0, 0),  # Red
        },
        {
            "type": "patient_f_young_follower",
            "x": 91,
            "y": 13,
        },
        {
            "type": "patient_f_follower",
            "x": 110,
            "y": 13,
            "encounter_message": "Da sind sie ja endlich!",
            "encounter_message_color": (255, 0, 0),  # Red
        },
        {
            "type": "patient_follower",
            "x": 125,
            "y": 13,
            "encounter_message": "Ich warte schon ewig!",
        },
        {
            "type": "patient_f_young_follower",
            "x": 150,
            "y": 13,
            "encounter_message": "Wann komm ich endlich dran?",
            "encounter_message_color": (255, 0, 0),  # Red
        },
        {
            "type": "doctor",
            "x": 150,
            "y": 13,
            "encounter_message": "Was machen Sie denn hier? \n Warum sind nicht auf Station?",
            "encounter_message_color": (0, 255, 0),  # Green
        },
    ],
    # Exit location - completing this returns to main level
    "exit_location": (160, 5),
    "background_music": "assets/music/house.ogg",  # Path relative to game root
    "background_image": "assets/backgrounds/Notaufnahme.png",
    "background_scroll_speed": 0.6,  # Optional: parallax scrolling speed (0.0 = static, 1.0 = moves with camera)
    "block_image": "block_white_2.png",  # Custom block image for this level
}

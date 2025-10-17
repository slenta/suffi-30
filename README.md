# suffi-30
level up through suffisuffzich's life by playing this simple jump n run game

## Features
- Dynamic platforming with moving platforms (linear & circular movement)
- Enemy AI with patrol, chase, and shooting behaviors
- Collectible weapons with different stats
- Power-ups and trophies
- Background music and sound effects
- Multiple levels with custom configurations

# HowToPlay
## Run default level (level1)
python launcher.py

## Run specific level
python launcher.py level1-advanced

## List all available levels
python launcher.py --list-levels

# Game Mechanics

## Moving Platforms (NEW!)
The game now supports moving platforms that can be configured in level files. See [MOVING_PLATFORMS.md](MOVING_PLATFORMS.md) for detailed documentation.

- **Linear Movement**: Platforms that move horizontally or vertically
- **Circular Movement**: Platforms that rotate in a circular pattern
- Players automatically move with the platform when standing on it
- Fully customizable speed, distance, and appearance

Example configuration:
```python
"moving_platform_locations": [
    {
        "x": 50, "y": 8,
        "platform_type": "grass",
        "movement_type": "linear",
        "speed": 1,
        "distance": 8,
        "direction": "horizontal"
    }
]
```

# Project Structure
```
suffi-30/
├── assets/                    # Centralized asset directory
│   ├── images/               # All game sprites and images
│   ├── backgrounds/          # Level background images
│   ├── music/                # Background music files (MP3, OGG)
│   ├── sounds/               # Sound effects (WAV, OGG)
│   ├── design/              # Source design files (piskel, afdesign)
│   └── renders/             # Rendered level previews
├── platformer/              # Game engine code
│   ├── levels/              # Level definitions
│   └── ...                  # Game modules
├── archive/                 # Archived old files
├── launcher.py              # Main game launcher
├── render_levels.py         # Level rendering utility
└── test_sound_system.py     # Sound system tester
```

# todo liste neu
- gameworld etwas höher gestalten

# Next ToDos
- change player image to suffi
- modify player image, strength, speed to level
- add weapons, which can be used when collected (Spraydose, Milchflasche etc.) -> was machen die?
- add End to Level --> Trophy collection, when coming to end with all trophys end level
- Minispiel im Level drin?
- level name/description am anfang einblenden 
- level ideas:
    - im club
    - im krankenhaus
    - im kindergarten
    - im schule
    - pubertät --> ziel an mama und papa vorbeizuschleichen
- Highscore wäre nice

# Sound System
The game now supports background music and sound effects!

## How to Add Music
1. Create MP3 files for your levels
2. Place them in the `assets/music/` directory:
   - `assets/music/level1.mp3` - for level1
   - `assets/music/level1-advanced.mp3` - for level1-advanced
3. Reference them in your level configuration

## How to Add Sound Effects
1. Place sound effect files in the `assets/sounds/` directory:
   - `assets/sounds/jump.wav` - player jump sound
   - `assets/sounds/gem_collect.wav` - gem collection sound
   - `assets/sounds/enemy_hit.wav` - enemy hit sound
   - And more (see assets/sounds/README.md for full list)

## Supported Audio Formats
- **Music**: MP3, OGG Vorbis, WAV
- **Sound Effects**: WAV (recommended), OGG Vorbis, MP3

## Volume Control
- Music volume: 70% by default
- Sound effects volume: 80% by default
- Both can be modified in the `SoundManager` class

## For New Levels
To add music to a new level, add this to your level configuration:
```python
level_config = {
    # ... your level data ...
    "background_music": "assets/music/your_level_music.mp3",
}
``` 

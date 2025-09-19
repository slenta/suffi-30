# suffi-30
level up through suffisuffzich's life by playing this simple jump n run game

# HowToPlay
## Run default level (level1)
python launcher.py

## Run specific level
python launcher.py level1-advanced

## List all available levels
python launcher.py --list-levels

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
2. Place them in the `music/` directory:
   - `music/level1.mp3` - for level1
   - `music/level1-advanced.mp3` - for level1-advanced
3. Or use absolute paths in your level configuration

## How to Add Sound Effects
1. Place sound effect files in the `sounds/` directory:
   - `sounds/jump.wav` - player jump sound
   - `sounds/gem_collect.wav` - gem collection sound
   - `sounds/enemy_hit.wav` - enemy hit sound
   - And more (see sounds/README.md for full list)

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
    "background_music": "music/your_level_music.mp3",  # or absolute path
}
``` 

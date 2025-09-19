# Sound Effects Directory

Place your sound effect files here:

## Required Sound Effects

The game will look for these sound effect files:

- `jump.wav` - Player jump sound
- `gem_collect.wav` - Sound when collecting gems
- `enemy_hit.wav` - Sound when hitting an enemy
- `player_hurt.wav` - Sound when player takes damage
- `player_death.wav` - Sound when player dies/falls down
- `powerup_collect.wav` - Sound when collecting power-ups
- `trophy_collect.wav` - Sound when collecting trophies
- `level_complete.wav` - Sound when completing a level
- `explode.wav` - Sound for explosions

## Supported Formats

- WAV (recommended for sound effects)
- OGG Vorbis
- MP3

## Notes

- If a sound file is missing, the game will continue without that sound effect
- No errors will be shown for missing sound files
- Sound effects can be disabled in the sound manager

## Volume Control

Sound effects volume is controlled separately from music and defaults to 80%.
You can modify the volume in the `SoundManager` class.
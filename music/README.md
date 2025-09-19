# Music Directory

Place your level-specific music files here:

## Supported Formats
- MP3 (recommended)
- OGG Vorbis
- WAV

## File Naming Convention
- `level1.mp3` - Background music for level1
- `level1-advanced.mp3` - Background music for level1-advanced
- Add more files for future levels

## Example Files Needed
You need to add these music files to enable background music:

1. **level1.mp3** - Music for the basic level1
   - Suggested style: Upbeat, beginner-friendly music
   
2. **level1-advanced.mp3** - Music for the advanced level
   - Suggested style: More intense, challenging music

## How to Add Custom Music
1. Place your MP3 files in this directory
2. The file paths are already configured in the level files:
   - `platformer/levels/level1.py` -> looks for `music/level1.mp3`
   - `platformer/levels/level1-advanced.py` -> looks for `music/level1-advanced.mp3`

## Alternative: Use Absolute Paths
You can also use absolute paths in your level configuration files if you want to store music elsewhere on your system.

Example in level file:
```python
"background_music": "/absolute/path/to/your/music/file.mp3"
```

## Volume Control
The sound system includes volume controls:
- Music volume: 0.7 (70%) by default
- You can modify this in the `SoundManager` class
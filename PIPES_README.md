# Pipe/Sub-Level System

This system allows you to create Mario-style pipes that lead to sub-levels, similar to the green pipes in Super Mario games.

## How It Works

1. **Main Level**: Contains pipes that the player can enter
2. **Sub-Level**: A separate level accessed through a pipe
3. **Return Mechanism**: When the sub-level is completed (exit reached), the player returns to the main level

## Creating a Sub-Level

Sub-levels are regular level files that start with `sub-` in their filename. These levels will **not** appear in the level selection menu.

Example: `platformer/levels/sub-cave.py`

```python
level_config = {
    "x_bounds": [-300, 2000],
    "y_bounds": [-200, 300],
    "player_spawn": (5, 1),  # Where player appears when entering
    "grass_locations": [(i, 14) for i in range(-20, 80)],
    "block_locations": [...],
    "gem_locations": [...],
    # ... other level configuration
    "exit_location": (70, 13),  # Completing this returns to main level
    "pipe_locations": [],  # Usually empty for sub-levels
}
```

## Adding Pipes to a Level

Add pipes to your level configuration using the `pipe_locations` key:

```python
level_config = {
    # ... other configuration ...
    
    "pipe_locations": [
        {
            "x": 30,                  # X position in grid units
            "y": 13 * 32,             # Y position in pixels (grid_y * 32)
            "sub_level": "sub-cave",  # Name of sub-level (without .py)
            "return_x": 32,           # Where player spawns when returning (grid units)
            "return_y": 13,           # Y position when returning (grid units)
            "direction": "down"       # Key to press: "down", "up", "left", "right"
        },
    ],
}
```

## Pipe Parameters

- **x**: X position in grid units (e.g., 30 = 30 * 32 pixels)
- **y**: Y position in pixels (usually `grid_y * 32`, e.g., `13 * 32` for ground level)
- **sub_level**: Name of the sub-level file without `.py` extension (e.g., "sub-cave" for `sub-cave.py`)
- **return_x**: X position (grid units) where player spawns when returning from sub-level
- **return_y**: Y position (grid units) where player spawns when returning
- **direction**: Which arrow key to press to enter ("down", "up", "left", "right")

## Player State Preservation

When entering and exiting sub-levels:
- **Preserved**: Gems, trophies, health, weapons
- **Location**: Player returns to the specified return position

Items collected in the sub-level are kept when returning to the main level!

## Example Levels

Check these example files:
- `platformer/levels/pipe-demo.py` - Main level with pipe
- `platformer/levels/sub-cave.py` - Sub-level example
- `platformer/levels/graffiti.py` - Updated with pipe support

## How to Use in Game

1. Walk up to a pipe
2. Press the directional key (e.g., DOWN arrow or S)
3. You'll be transported to the sub-level
4. Complete the sub-level (reach the exit)
5. You'll return to the main level at the return position

## Tips

- Sub-levels can be smaller and more focused than main levels
- Use sub-levels for bonus challenges, secret areas, or puzzles
- You can have multiple pipes in one level leading to different sub-levels
- Sub-levels can also have their own pipes (but be careful with nesting!)
- The pipe image currently uses the door sprite - you can customize this in `pipe.py`

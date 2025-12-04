# Teil Collectible - Radial Blur Effect

## Overview
The "Teil" collectible (power-up type 5) creates a radial blur effect where only the area around the player remains sharp, while the rest of the screen is blurred. This effect lasts for 15 seconds.

## How to Add to Your Level

Add a power-up with type 5 to your level configuration:

```python
"powerups": [
    {"x": 50, "y": 10, "type": 5}  # Teil collectible at grid position (50, 10)
]
```

## Technical Details

- **Duration**: 15 seconds (900 frames at 60 FPS)
- **Effect**: Radial blur centered on the player
- **Sharp Radius**: 150 pixels around the player
- **Blur Strength**: 10x downscaling for blur effect
- **Image**: `platformer/assets/images/powerups/powerup-pill.png`

## Configuration Constants

You can adjust these values in `platformer/config/constants.py`:

```python
RADIAL_BLUR_DURATION = 900  # Frames (15 seconds at 60 FPS)
RADIAL_BLUR_RADIUS = 150    # Pixels - radius of sharp area around player
RADIAL_BLUR_STRENGTH = 10   # Blur strength (higher = more blur)
```

## Implementation

The radial blur effect:
1. Creates a blurred version of the screen by downscaling and upscaling
2. Generates a radial gradient mask centered on the player
3. Blends the blurred version based on distance from the player
4. Sharp area within RADIAL_BLUR_RADIUS, gradually blurs outward

## Example Level Usage

```python
level_config = {
    "platforms": [...],
    "powerups": [
        {"x": 30, "y": 10, "type": 1},  # Speed boost
        {"x": 50, "y": 10, "type": 5},  # Teil - radial blur effect
        {"x": 70, "y": 10, "type": 0}   # Size boost
    ],
    # ... rest of level config
}
```

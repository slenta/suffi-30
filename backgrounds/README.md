# Backgrounds Directory

Place your background images here for use in levels.

## Background Images

The game will look for background image files specified in level configurations:

- `level1_bg.png` - Background for level1
- `level1-advanced_bg.png` - Background for level1-advanced
- Add more as needed for new levels

## Supported Formats

- PNG (recommended for transparency support)
- JPG/JPEG
- BMP
- GIF (non-animated)

## Image Guidelines

### Dimensions
- **Height**: Should match your target screen height (800px recommended)
- **Width**: Can be any width - will tile horizontally if needed
- For seamless tiling, make sure the left and right edges match

### Design Tips
- Use horizontal landscapes that can tile seamlessly
- Consider parallax scrolling effect (slower background movement)
- Avoid too much detail that might distract from gameplay
- Use complementary colors to your game sprites

## Configuration

In your level files, add:

```python
level_config = {
    # ... other level data ...
    "background_image": "backgrounds/your_background.png",
    "background_scroll_speed": 0.3,  # Optional: 0.0 = static, 1.0 = moves with camera
}
```

## Parallax Scrolling

The `background_scroll_speed` parameter controls how the background moves:

- `0.0` - Background stays completely static
- `0.5` - Background moves at half the camera speed (default)
- `1.0` - Background moves at same speed as camera
- Values between create different parallax effects

## Fallback

If no background image is specified or the file is missing, the game will use the default blue sky color (`BG_COLOR` in settings).
# Level Renderer for 2D Platformer Game

This tool renders your platformer levels as PNG images for easy level design visualization and review.

## Features

- **Visual Level Overview**: See your entire level layout at a glance
- **Color-coded Elements**: Different colors and shapes for each game element
- **Grid Lines**: Optional grid overlay to help with tile alignment
- **Legend**: Built-in legend explaining all visual elements
- **Flexible Output**: Choose specific levels or render all at once

## Usage

### Render All Levels
```bash
python render_levels.py
```

### Render Specific Level
```bash
python render_levels.py level1.py
# or
python render_levels.py platformer/levels/level2.py
```

### Additional Options
```bash
# Render without grid lines
python render_levels.py --no-grid

# Specify custom output directory
python render_levels.py --output-dir my_level_images

# Combine options
python render_levels.py level2.py --no-grid --output-dir clean_renders
```

## Visual Legend

The rendered images use the following color scheme:

- 🟢 **Green Rectangles**: Grass platforms
- 🟤 **Brown Rectangles**: Block platforms  
- 🟡 **Gold Circles**: Gems (collectibles)
- 🟠 **Orange Circles**: Trophies
- 🟣 **Magenta Shapes**: Power-ups
  - Squares: Size power-ups (type 0)
  - Diamonds: Speed power-ups (type 1)
- 🔴 **Red Triangles**: Enemies (with patrol range lines)
- 🟢 **Green Star**: Level exit
- 🔵 **Blue Circle**: Player start position

## Enemy Information

Enemy triangles show:
- **Size**: Triangle size reflects the enemy's size multiplier
- **Patrol Range**: Horizontal lines below enemies show their patrol area
- **Position**: Current spawn position in the level

## Requirements

- Python 3.6+
- PIL/Pillow library (for image generation)

Install Pillow if needed:
```bash
pip install Pillow
```

## Output

Images are saved as PNG files in the `level_renders/` directory (or your specified output directory). Each level generates a file named `{level_name}_render.png`.

## Tips for Level Design

1. **Use the grid** to ensure proper tile alignment
2. **Check enemy patrol ranges** don't overlap problematically  
3. **Verify gem/trophy placement** for balanced rewards
4. **Review platforming flow** from start to exit
5. **Ensure power-ups are strategically placed** before difficult sections

## Troubleshooting

- **"No level files found"**: Make sure you're running from the game root directory
- **Import errors**: Ensure PIL/Pillow is installed (`pip install Pillow`)
- **Level loading errors**: Check that your level files have valid Python syntax
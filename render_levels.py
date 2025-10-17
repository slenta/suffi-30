#!/usr/bin/env python3
"""
Level Renderer for 2D Platformer Game

This script renders all levels in the platformer/levels/ directory as PNG images
for visual level design review.

Usage:
    python render_levels.py                    # Render all levels
    python render_levels.py level1.py          # Render specific level
    python render_levels.py --no-grid          # Render without grid lines
"""

import os
import sys
import importlib.util
from PIL import Image, ImageDraw
import glob
import argparse

# Game constants (from settings.py)
GRIDSIZE = 18
DEFAULT_TILE_SIZE = 18

# Image cache to avoid loading the same image multiple times
IMAGE_CACHE = {}


def load_sprite_image(image_path, size=None):
    """Load and cache sprite images."""
    if image_path in IMAGE_CACHE:
        return IMAGE_CACHE[image_path]

    try:
        # Try different possible paths
        possible_paths = [
            image_path,
            f"platformer/{image_path}",
            f"platformer/data/images/{image_path}",
            f"platformer/data/images/{os.path.basename(image_path)}",
        ]

        image = None
        for path in possible_paths:
            if os.path.exists(path):
                image = Image.open(path).convert("RGBA")
                break

        if image is None:
            print(f"Warning: Could not find image {image_path}, using fallback")
            # Create a fallback colored rectangle
            fallback_size = size or (GRIDSIZE, GRIDSIZE)
            image = Image.new(
                "RGBA", fallback_size, (255, 0, 255, 255)
            )  # Magenta fallback

        # Resize if size specified
        if size and image.size != size:
            image = image.resize(size, Image.Resampling.LANCZOS)

        IMAGE_CACHE[image_path] = image
        return image

    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        # Return fallback image
        fallback_size = size or (GRIDSIZE, GRIDSIZE)
        fallback = Image.new("RGBA", fallback_size, (255, 0, 255, 255))
        IMAGE_CACHE[image_path] = fallback
        return fallback


# Color definitions for different elements
COLORS = {
    "background": (135, 206, 235),  # Sky blue
    "grass": (34, 139, 34),  # Forest green
    "block": (139, 69, 19),  # Saddle brown
    "gem": (255, 215, 0),  # Gold
    "powerup": (255, 0, 255),  # Magenta
    "enemy": (255, 0, 0),  # Red
    "trophy": (255, 165, 0),  # Orange
    "exit": (0, 255, 0),  # Bright green
    "player_start": (0, 0, 255),  # Blue
}


def load_level_config(level_file):
    """Load level configuration from a Python file."""
    try:
        spec = importlib.util.spec_from_file_location("level", level_file)
        if spec is None or spec.loader is None:
            print(f"Could not load spec for {level_file}")
            return None
        level_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(level_module)
        return level_module.level_config
    except Exception as e:
        print(f"Error loading level config from {level_file}: {e}")
        return None


def calculate_level_bounds(level_config):
    """Calculate the pixel bounds for rendering the level based on actual content."""
    # Collect all object positions to find actual bounds
    all_x_coords = []
    all_y_coords = []

    # Add player start position
    all_x_coords.extend([5])  # PLAYER_START_X from settings
    all_y_coords.extend([1])  # PLAYER_START_Y from settings

    # Collect grass locations
    grass_locations = level_config.get("grass_locations", [])
    for x, y in grass_locations:
        all_x_coords.append(x)
        all_y_coords.append(y)

    # Collect block locations
    block_locations = level_config.get("block_locations", [])
    for x, y in block_locations:
        all_x_coords.append(x)
        all_y_coords.append(y)

    # Collect gem locations
    gem_locations = level_config.get("gem_locations", [])
    for x, y in gem_locations:
        all_x_coords.append(x)
        all_y_coords.append(y)

    # Collect trophy locations
    trophy_locations = level_config.get("trophy_locations", [])
    for x, y in trophy_locations:
        all_x_coords.append(x)
        all_y_coords.append(y)

    # Collect powerup locations
    powerup_locations = level_config.get("powerup_locations", [])
    for powerup in powerup_locations:
        all_x_coords.append(powerup["x"])
        all_y_coords.append(powerup["y"])

    # Collect enemy locations
    enemy_locations = level_config.get("enemy_locations", [])
    for enemy in enemy_locations:
        all_x_coords.append(enemy["x"])
        all_y_coords.append(enemy["y"])

    # Collect exit location
    exit_location = level_config.get("exit_location")
    if exit_location:
        all_x_coords.append(exit_location[0])
        all_y_coords.append(exit_location[1])

    # Calculate bounds with some padding
    if not all_x_coords or not all_y_coords:
        # Fallback to default bounds if no content found
        min_x, max_x = -10, 50
        min_y, max_y = -5, 20
    else:
        min_x = min(all_x_coords) - 2  # 2 tile padding
        max_x = max(all_x_coords) + 2
        min_y = min(all_y_coords) - 2
        max_y = max(all_y_coords) + 2

    # Convert to pixel coordinates
    pixel_min_x = min_x * GRIDSIZE
    pixel_max_x = max_x * GRIDSIZE
    pixel_min_y = min_y * GRIDSIZE
    pixel_max_y = max_y * GRIDSIZE

    width = pixel_max_x - pixel_min_x
    height = pixel_max_y - pixel_min_y

    return pixel_min_x, pixel_min_y, width, height


def world_to_image_coords(x, y, min_x, min_y):
    """Convert world coordinates to image coordinates."""
    return x * GRIDSIZE - min_x, y * GRIDSIZE - min_y


def draw_grid(draw, min_x, min_y, width, height):
    """Draw a light grid to help visualize tile boundaries."""
    grid_color = (200, 200, 200, 100)  # Light gray, semi-transparent

    # Vertical lines
    for x in range(0, width, GRIDSIZE):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)

    # Horizontal lines
    for y in range(0, height, GRIDSIZE):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)


def draw_platforms(draw, image, locations, min_x, min_y, sprite_name, size=GRIDSIZE):
    """Draw platforms (grass or blocks) using actual sprites."""
    sprite_image = load_sprite_image(sprite_name, (size, size))

    for x, y in locations:
        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)
        image.paste(sprite_image, (img_x, img_y), sprite_image)


def draw_items_with_sprites(
    draw, image, locations, min_x, min_y, sprite_name, size=None
):
    """Draw items (gems, trophies) using actual sprites."""
    item_size = size or (GRIDSIZE, GRIDSIZE)
    sprite_image = load_sprite_image(sprite_name, item_size)

    for x, y in locations:
        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)
        # Center the item in the tile
        center_x = img_x + GRIDSIZE // 2 - item_size[0] // 2
        center_y = img_y + GRIDSIZE // 2 - item_size[1] // 2
        image.paste(sprite_image, (center_x, center_y), sprite_image)


def draw_powerups_with_sprites(draw, image, powerup_locations, min_x, min_y):
    """Draw powerups using actual sprites."""
    for powerup in powerup_locations:
        x, y = powerup["x"], powerup["y"]
        powerup_type = powerup.get("type", 0)

        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)

        # Different sprites for different powerup types
        if powerup_type == 0:  # Size powerup
            sprite_name = "pulver.png"  # or whatever sprite you use for size powerup
        elif powerup_type == 1:  # Speed powerup
            sprite_name = "banana.png"  # or whatever sprite you use for size powerup
        else:  # Speed powerup
            sprite_name = "powerups/powerup-pill.png"  # or whatever sprite you use for speed powerup

        powerup_image = load_sprite_image(sprite_name, (GRIDSIZE, GRIDSIZE))
        center_x = img_x + GRIDSIZE // 2 - GRIDSIZE // 2
        center_y = img_y + GRIDSIZE // 2 - GRIDSIZE // 2
        image.paste(powerup_image, (center_x, center_y), powerup_image)


def draw_enemies_with_sprites(draw, image, enemy_locations, min_x, min_y):
    """Draw enemies using actual sprites."""
    for enemy in enemy_locations:
        x, y = enemy["x"], enemy["y"]
        enemy_image_name = enemy.get("image", "trump.png")
        size_mult = enemy.get("size_multiplier", 1)

        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)

        # Size based on multiplier
        enemy_size = int(GRIDSIZE * size_mult)
        enemy_image = load_sprite_image(enemy_image_name, (enemy_size, enemy_size))

        center_x = img_x + GRIDSIZE // 2 - enemy_size // 2
        center_y = img_y + GRIDSIZE // 2 - enemy_size // 2
        image.paste(enemy_image, (center_x, center_y), enemy_image)

        # Add patrol range visualization (optional thin line)
        patrol_range = enemy.get("patrol_range", 50)
        patrol_pixels = patrol_range
        center_sprite_x = center_x + enemy_size // 2
        center_sprite_y = center_y + enemy_size + 5
        draw.line(
            [
                center_sprite_x - patrol_pixels // 2,
                center_sprite_y,
                center_sprite_x + patrol_pixels // 2,
                center_sprite_y,
            ],
            fill=(255, 0, 0, 128),
            width=1,
        )


def draw_special_locations_with_sprites(
    draw, image, locations, min_x, min_y, sprite_name, fallback_color
):
    """Draw special locations like exit or player start using sprites."""
    for location in locations:
        if isinstance(location, tuple):
            x, y = location
        else:
            x, y = location["x"], location["y"]

        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)

        try:
            sprite_image = load_sprite_image(sprite_name, (GRIDSIZE, GRIDSIZE))
            center_x = img_x + GRIDSIZE // 2 - GRIDSIZE // 2
            center_y = img_y + GRIDSIZE // 2 - GRIDSIZE // 2
            image.paste(sprite_image, (center_x, center_y), sprite_image)
        except:
            # Fallback to colored shape if sprite not found
            center_x = img_x + GRIDSIZE // 2
            center_y = img_y + GRIDSIZE // 2
            size = GRIDSIZE // 2
            draw.ellipse(
                [
                    center_x - size // 2,
                    center_y - size // 2,
                    center_x + size // 2,
                    center_y + size // 2,
                ],
                fill=fallback_color,
                outline=(0, 0, 0),
                width=3,
            )


def render_level(level_config, output_path, show_grid=True):
    """Render a single level configuration to a PNG image."""
    try:
        # Calculate image dimensions
        min_x, min_y, width, height = calculate_level_bounds(level_config)

        # Create image
        image = Image.new("RGB", (width, height), COLORS["background"])
        draw = ImageDraw.Draw(image)

        # Draw grid lines (optional - light gray)
        if show_grid:
            draw_grid(draw, min_x, min_y, width, height)

        # Draw grass using actual sprites
        grass_locations = level_config.get("grass_locations", [])
        draw_platforms(draw, image, grass_locations, min_x, min_y, "grass_02.png")

        # Draw blocks using actual sprites
        block_locations = level_config.get("block_locations", [])
        draw_platforms(draw, image, block_locations, min_x, min_y, "block_00.png")

        # Draw gems using actual sprites
        gem_locations = level_config.get("gem_locations", [])
        draw_items_with_sprites(draw, image, gem_locations, min_x, min_y, "gem.png")

        # Draw trophies using actual sprites
        trophy_locations = level_config.get("trophy_locations", [])
        trophy_image = level_config.get("trophy_image", "trophy.png")
        # Extract just the filename if it's a path
        trophy_sprite = os.path.basename(trophy_image) if trophy_image else "trophy.png"
        draw_items_with_sprites(
            draw, image, trophy_locations, min_x, min_y, trophy_sprite
        )

        # Draw powerups using actual sprites
        powerup_locations = level_config.get("powerup_locations", [])
        draw_powerups_with_sprites(draw, image, powerup_locations, min_x, min_y)

        # Draw enemies using actual sprites
        enemy_locations = level_config.get("enemy_locations", [])
        draw_enemies_with_sprites(draw, image, enemy_locations, min_x, min_y)

        # Draw exit using actual sprites
        exit_location = level_config.get("exit_location")
        if exit_location:
            draw_special_locations_with_sprites(
                draw,
                image,
                [exit_location],
                min_x,
                min_y,
                "door_open.png",
                COLORS["exit"],
            )

        # Draw player start position using actual sprites
        player_start = [(5, 1)]  # From PLAYER_START_X, PLAYER_START_Y in settings
        draw_special_locations_with_sprites(
            draw,
            image,
            player_start,
            min_x,
            min_y,
            "suffi_00.png",
            COLORS["player_start"],
        )

        # Add legend
        draw_legend(draw, width, height)

        # Add level information
        draw_level_info(draw, level_config, width)

        # Save image
        image.save(output_path)
        print(f"Level rendered successfully: {output_path}")
        print(f"  Dimensions: {width}x{height} pixels")
        return True

    except Exception as e:
        print(f"Error rendering level: {e}")
        return False


def draw_legend(draw, width, height):
    """Draw a simple legend explaining the sprites."""
    legend_items = [
        ("Grass", COLORS["grass"]),
        ("Blocks", COLORS["block"]),
        ("Gems", COLORS["gem"]),
        ("Trophies", COLORS["trophy"]),
        ("Powerups", COLORS["powerup"]),
        ("Enemies", COLORS["enemy"]),
        ("Exit", COLORS["exit"]),
        ("Player", COLORS["player_start"]),
    ]

    legend_x = 10
    legend_y = height - 20 - len(legend_items) * 15

    # Background for legend
    legend_width = 100
    legend_height = len(legend_items) * 15 + 10
    draw.rectangle(
        [legend_x - 5, legend_y - 5, legend_x + legend_width, legend_y + legend_height],
        fill=(255, 255, 255, 230),
        outline=(0, 0, 0),
    )

    for i, (name, color) in enumerate(legend_items):
        y = legend_y + i * 15
        # Draw simple colored rectangle as legend indicator
        draw.rectangle(
            [legend_x, y, legend_x + 12, y + 12], fill=color, outline=(0, 0, 0)
        )


def draw_level_info(draw, level_config, width):
    """Draw level statistics in the top-right corner."""
    # Count various elements
    gem_count = len(level_config.get("gem_locations", []))
    trophy_count = len(level_config.get("trophy_locations", []))
    enemy_count = len(level_config.get("enemy_locations", []))
    powerup_count = len(level_config.get("powerup_locations", []))

    info_lines = [
        f"Gems: {gem_count}",
        f"Trophies: {trophy_count}",
        f"Enemies: {enemy_count}",
        f"Powerups: {powerup_count}",
    ]

    # Position in top-right
    info_width = 120
    info_height = len(info_lines) * 15 + 10
    info_x = width - info_width - 10
    info_y = 10

    # Background
    draw.rectangle(
        [info_x - 5, info_y - 5, info_x + info_width, info_y + info_height],
        fill=(255, 255, 255, 230),
        outline=(0, 0, 0),
    )

    # Just draw colored indicators for now (text rendering in PIL is complex)
    for i, line in enumerate(info_lines):
        y = info_y + i * 15
        # Draw a small colored square to indicate the category
        colors = [COLORS["gem"], COLORS["trophy"], COLORS["enemy"], COLORS["powerup"]]
        if i < len(colors):
            draw.rectangle(
                [info_x, y, info_x + 12, y + 12], fill=colors[i], outline=(0, 0, 0)
            )


def main():
    """Main function to render all levels."""
    parser = argparse.ArgumentParser(
        description="Render platformer levels as PNG images"
    )
    parser.add_argument(
        "level_file", nargs="?", help="Specific level file to render (e.g., level1.py)"
    )
    parser.add_argument(
        "--no-grid", action="store_true", help="Disable grid lines in output"
    )
    parser.add_argument(
        "--output-dir",
        default="level_renders",
        help="Output directory for rendered images",
    )

    args = parser.parse_args()

    # Determine which level files to process
    if args.level_file:
        # Single level specified
        if os.path.exists(args.level_file):
            level_files = [args.level_file]
        elif os.path.exists(f"platformer/levels/{args.level_file}"):
            level_files = [f"platformer/levels/{args.level_file}"]
        else:
            print(f"Level file not found: {args.level_file}")
            return
    else:
        # Find all level files
        level_files = glob.glob("platformer/levels/level*.py")

    if not level_files:
        print("No level files found in platformer/levels/")
        return

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Render each level
    successful_renders = 0
    for level_file in sorted(level_files):
        print(f"Processing {level_file}...")

        # Load level configuration
        level_config = load_level_config(level_file)
        if level_config is None:
            continue

        # Generate output filename
        level_name = os.path.splitext(os.path.basename(level_file))[0]
        output_path = os.path.join(args.output_dir, f"{level_name}_render.png")

        # Render level
        if render_level(level_config, output_path, show_grid=not args.no_grid):
            successful_renders += 1

    print(
        f"\nRendering complete! {successful_renders}/{len(level_files)} levels rendered successfully."
    )
    print(f"Output images saved in '{args.output_dir}/' directory.")


if __name__ == "__main__":
    main()

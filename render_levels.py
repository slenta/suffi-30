#!/usr/bin/env python3
"""
Level Renderer for 2D Platformer Game

This script renders all levels in the platformer/levels/ directory as PNG images
for visual level design review.

Usage:
    python render_levels.py                    # Render all levels
    python render_levels.py level1.py          # Render specific level
    python render_levels.py --no-grid          # Render without grid lines
    python render_levels.py --bg-opacity 0.5   # Render with 50% background opacity
"""

import os
import sys
import importlib.util
from PIL import Image, ImageDraw, ImageFont
import glob
import argparse

# Add platformer directory to path to import enemy config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "platformer"))
try:
    from config.enemy_config import ENEMY_TYPES
except ImportError:
    print(
        "Warning: Could not import enemy_config, enemy sprites may not render correctly"
    )
    ENEMY_TYPES = {}

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
        # Try different possible paths (updated for centralized assets)
        possible_paths = [
            image_path,
            f"platformer/assets/images/{image_path}",
            f"platformer/assets/images/{os.path.basename(image_path)}",
            f"platformer/assets/backgrounds/{image_path}",
            f"platformer/assets/backgrounds/{os.path.basename(image_path)}",
            f"assets/images/{image_path}",
            f"assets/images/{os.path.basename(image_path)}",
            f"assets/backgrounds/{image_path}",
            f"assets/backgrounds/{os.path.basename(image_path)}",
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
    "moving_platform": (100, 100, 200),  # Light blue
    "weapon": (255, 215, 0),  # Gold
    "pipe": (0, 200, 0),  # Green
    "spike": (255, 50, 50),  # Bright red
    "ladder": (139, 90, 43),  # Brown
    "waterfall": (64, 164, 223),  # Water blue
    "moving_platform_path": (200, 200, 200, 100),  # Light gray, semi-transparent
    "death_zone": (255, 0, 0, 50),  # Red, very transparent
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

    # Collect weapon locations
    weapon_locations = level_config.get("weapon_locations", [])
    for weapon in weapon_locations:
        all_x_coords.append(weapon["x"])
        all_y_coords.append(weapon["y"])

    # Collect pipe locations
    pipe_locations = level_config.get("pipe_locations", [])
    for pipe in pipe_locations:
        all_x_coords.append(pipe["x"])
        all_y_coords.append(pipe["y"])

    # Collect spike locations
    spike_locations = level_config.get("spike_locations", [])
    for spike_loc in spike_locations:
        if isinstance(spike_loc, tuple):
            x, y = spike_loc
        else:
            x, y = spike_loc["x"], spike_loc["y"]
        all_x_coords.append(x)
        all_y_coords.append(y)

    # Collect ladder locations
    ladder_locations = level_config.get("ladder_locations", [])
    for ladder_loc in ladder_locations:
        if isinstance(ladder_loc, tuple):
            x, y = ladder_loc
        else:
            x, y = ladder_loc["x"], ladder_loc["y"]
        all_x_coords.append(x)
        all_y_coords.append(y)

    # Collect waterfall locations
    waterfall_locations = level_config.get("waterfall_locations", [])
    for waterfall_loc in waterfall_locations:
        if isinstance(waterfall_loc, tuple):
            x, y = waterfall_loc
        else:
            x, y = waterfall_loc["x"], waterfall_loc["y"]
        all_x_coords.append(x)
        all_y_coords.append(y)

    # Collect moving platform locations (including their movement range)
    moving_platform_locations = level_config.get("moving_platform_locations", [])
    for platform in moving_platform_locations:
        x, y = platform["x"], platform["y"]
        distance = platform.get("distance", 0)
        direction = platform.get("direction", "horizontal")
        movement_type = platform.get("movement_type", "linear")

        all_x_coords.append(x)
        all_y_coords.append(y)

        # Add the endpoint of platform movement
        if movement_type == "linear":
            if direction == "horizontal":
                all_x_coords.append(x + distance)
            elif direction == "vertical":
                all_y_coords.append(y + distance)
        elif movement_type == "circular":
            # For circular, add the radius in all directions
            all_x_coords.extend([x - distance, x + distance])
            all_y_coords.extend([y - distance, y + distance])

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
    """Draw a light grid to help visualize tile boundaries with coordinate labels."""
    grid_color = (200, 200, 200, 100)  # Light gray, semi-transparent
    coord_color = (50, 50, 50)  # Dark gray for text

    # Try to load a larger font, fallback to default if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", 20)
        except:
            font = ImageFont.load_default()

    # Calculate the starting grid coordinates
    start_x_coord = min_x // GRIDSIZE
    start_y_coord = min_y // GRIDSIZE

    # Vertical lines with x-coordinate labels
    for i, x in enumerate(range(0, width, GRIDSIZE)):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
        # Draw x-coordinate label every 5 tiles to avoid clutter
        if i % 5 == 0:
            coord_label = str(start_x_coord + i)
            # Draw text at top and bottom of image
            draw.text((x + 2, 2), coord_label, fill=coord_color, font=font)
            if height > 30:
                draw.text(
                    (x + 2, height - 25), coord_label, fill=coord_color, font=font
                )

    # Horizontal lines with y-coordinate labels
    for i, y in enumerate(range(0, height, GRIDSIZE)):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
        # Draw y-coordinate label every 5 tiles to avoid clutter
        if i % 5 == 0:
            coord_label = str(start_y_coord + i)
            # Draw text at left and right of image
            draw.text((2, y + 2), coord_label, fill=coord_color, font=font)
            if width > 30:
                draw.text((width - 30, y + 2), coord_label, fill=coord_color, font=font)

            # Draw y-axis coordinate labels every 50 x pixels
            for x in range(50, width, 500):
                draw.text((x + 2, y + 2), coord_label, fill=coord_color, font=font)


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
        if powerup_type == 0 or powerup_type == "bigger":  # Size powerup
            sprite_name = "pulver.png"
        elif powerup_type == 1 or powerup_type == "faster":  # Speed powerup
            sprite_name = "banana.png"
        elif powerup_type == 2:  # Another powerup type
            sprite_name = "spraydose.png"
        else:  # Generic powerup
            sprite_name = "powerups/powerup-pill.png"

        powerup_image = load_sprite_image(sprite_name, (GRIDSIZE, GRIDSIZE))
        center_x = img_x + GRIDSIZE // 2 - GRIDSIZE // 2
        center_y = img_y + GRIDSIZE // 2 - GRIDSIZE // 2
        image.paste(powerup_image, (center_x, center_y), powerup_image)


def draw_weapons_with_sprites(draw, image, weapon_locations, min_x, min_y):
    """Draw weapon pickups using actual sprites."""
    for weapon in weapon_locations:
        x, y = weapon["x"], weapon["y"]
        weapon_type = weapon.get("type", "wasserpistole")

        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)

        # Map weapon types to their sprites
        weapon_sprites = {
            "wasserpistole": "weapons/wasserpistole.png",
            "milchflasche": "weapons/milkbottle-closed.png",
            "schwert": "weapons/baseball-bat.png",  # Using bat as placeholder
            "gun": "weapons/wasserpistole.png",  # Fallback
        }

        sprite_name = weapon_sprites.get(weapon_type, "weapons/wasserpistole.png")

        # Weapons are typically 2x size
        weapon_size = int(GRIDSIZE * 2)
        weapon_image = load_sprite_image(sprite_name, (weapon_size, weapon_size))

        center_x = img_x + GRIDSIZE // 2 - weapon_size // 2
        center_y = img_y + GRIDSIZE // 2 - weapon_size // 2
        image.paste(weapon_image, (center_x, center_y), weapon_image)


def draw_moving_platforms_with_sprites(draw, image, platform_locations, min_x, min_y):
    """Draw moving platforms and their movement paths."""
    for platform_config in platform_locations:
        x, y = platform_config["x"], platform_config["y"]
        platform_type = platform_config.get("platform_type", "grass")
        movement_type = platform_config.get("movement_type", "linear")
        distance = platform_config.get("distance", 0)
        direction = platform_config.get("direction", "horizontal")

        # Choose sprite based on platform type
        if platform_type == "grass":
            sprite_name = "grass_02.png"
        else:
            sprite_name = "block_00.png"

        platform_image = load_sprite_image(sprite_name, (GRIDSIZE, GRIDSIZE))

        # Draw the platform at start position
        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)
        image.paste(platform_image, (img_x, img_y), platform_image)

        # Draw movement path visualization
        if movement_type == "linear":
            start_x, start_y = img_x + GRIDSIZE // 2, img_y + GRIDSIZE // 2

            if direction == "horizontal":
                end_x = start_x + (distance * GRIDSIZE)
                end_y = start_y
                # Draw horizontal dashed line
                for i in range(0, int(distance * GRIDSIZE), 10):
                    draw.line(
                        [(start_x + i, start_y), (start_x + i + 5, start_y)],
                        fill=(150, 150, 255, 200),
                        width=2,
                    )
                # Draw end position marker
                draw.ellipse(
                    [end_x - 3, end_y - 3, end_x + 3, end_y + 3],
                    fill=COLORS["moving_platform"],
                    outline=(0, 0, 0),
                )
            elif direction == "vertical":
                end_x = start_x
                end_y = start_y + (distance * GRIDSIZE)
                # Draw vertical dashed line
                for i in range(0, int(distance * GRIDSIZE), 10):
                    draw.line(
                        [(start_x, start_y + i), (start_x, start_y + i + 5)],
                        fill=(150, 150, 255, 200),
                        width=2,
                    )
                # Draw end position marker
                draw.ellipse(
                    [end_x - 3, end_y - 3, end_x + 3, end_y + 3],
                    fill=COLORS["moving_platform"],
                    outline=(0, 0, 0),
                )

        elif movement_type == "circular":
            center_x = img_x + GRIDSIZE // 2
            center_y = img_y + GRIDSIZE // 2
            radius = distance * GRIDSIZE

            # Draw circular path
            draw.ellipse(
                [
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                ],
                outline=(150, 150, 255, 200),
                width=2,
            )

        # Add arrow indicator for direction
        center_x = img_x + GRIDSIZE // 2
        center_y = img_y + GRIDSIZE // 2
        arrow_size = 4

        if movement_type == "linear" and direction == "horizontal":
            # Right arrow
            draw.polygon(
                [
                    (center_x + 2, center_y - arrow_size),
                    (center_x + 2 + arrow_size, center_y),
                    (center_x + 2, center_y + arrow_size),
                ],
                fill=(255, 255, 0),
            )
        elif movement_type == "linear" and direction == "vertical":
            # Down arrow
            draw.polygon(
                [
                    (center_x - arrow_size, center_y + 2),
                    (center_x, center_y + 2 + arrow_size),
                    (center_x + arrow_size, center_y + 2),
                ],
                fill=(255, 255, 0),
            )
        elif movement_type == "circular":
            # Circular arrow indicator
            draw.ellipse(
                [center_x - 2, center_y - 2, center_x + 2, center_y + 2],
                fill=(255, 255, 0),
                outline=(0, 0, 0),
            )


def draw_enemies_with_sprites(draw, image, enemy_locations, min_x, min_y):
    """Draw enemies using actual sprites from enemy config."""
    for enemy in enemy_locations:
        x, y = enemy["x"], enemy["y"]

        # Check if enemy has a type field that references enemy config
        enemy_type = enemy.get("type")
        if enemy_type and enemy_type in ENEMY_TYPES:
            # Get config from ENEMY_TYPES and merge with any overrides from level
            enemy_config = ENEMY_TYPES[enemy_type].copy()
            # Override with any custom values from the level config
            for key, value in enemy.items():
                if key not in ["x", "y", "type"]:  # Don't override position or type
                    enemy_config[key] = value

            enemy_image_name = enemy_config.get("image", "trump.png")
            size_mult = enemy_config.get("size_multiplier", 1)
            patrol_range = enemy_config.get("patrol_range", 50)
        else:
            # Fallback to direct values if no type specified or type not found
            enemy_image_name = enemy.get("image", "trump.png")
            size_mult = enemy.get("size_multiplier", 1)
            patrol_range = enemy.get("patrol_range", 50)

        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)

        # Size based on multiplier
        enemy_size = int(GRIDSIZE * size_mult)
        enemy_image = load_sprite_image(enemy_image_name, (enemy_size, enemy_size))

        center_x = img_x + GRIDSIZE // 2 - enemy_size // 2
        center_y = img_y + GRIDSIZE // 2 - enemy_size // 2
        image.paste(enemy_image, (center_x, center_y), enemy_image)

        # Add patrol range visualization (optional thin line)
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


def draw_ladders_with_sprites(draw, image, ladder_locations, min_x, min_y):
    """Draw ladders using actual sprites."""
    for ladder_loc in ladder_locations:
        if isinstance(ladder_loc, tuple):
            x, y = ladder_loc
        else:
            x, y = ladder_loc["x"], ladder_loc["y"]

        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)

        # Load ladder sprite
        ladder_image = load_sprite_image("ladder/ladder_02.png", (GRIDSIZE, GRIDSIZE))
        image.paste(ladder_image, (img_x, img_y), ladder_image)


def draw_waterfalls_with_sprites(draw, image, waterfall_locations, min_x, min_y):
    """Draw waterfalls using actual sprites."""
    for waterfall_loc in waterfall_locations:
        if isinstance(waterfall_loc, tuple):
            x, y = waterfall_loc
        else:
            x, y = waterfall_loc["x"], waterfall_loc["y"]

        img_x, img_y = world_to_image_coords(x, y, min_x, min_y)

        # Load waterfall sprite
        waterfall_image = load_sprite_image(
            "waterfall/waterfall_01.png", (GRIDSIZE, GRIDSIZE)
        )
        image.paste(waterfall_image, (img_x, img_y), waterfall_image)


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


def create_background_image(level_config, width, height, opacity=0.3):
    """Create the base image with background, mimicking pygame's rendering.

    Args:
        level_config: Level configuration dictionary
        width: Canvas width in pixels
        height: Canvas height in pixels
        opacity: Background image opacity (0.0 to 1.0, default 1.0)
    """
    # Check if level has a background image specified
    bg_image_path = level_config.get("background_image")

    if bg_image_path:
        # Try to load the background image
        try:
            # Try different possible paths
            possible_paths = [
                bg_image_path,
                f"platformer/{bg_image_path}",
                f"{bg_image_path}",
            ]

            background = None
            for path in possible_paths:
                if os.path.exists(path):
                    background = Image.open(path).convert("RGBA")
                    print(f"  Loaded background image: {path}")
                    break

            if background is not None:
                # Create a canvas of the level size
                canvas = Image.new("RGB", (width, height), COLORS["background"])

                # Apply opacity to background if needed
                if opacity < 1.0:
                    # Adjust alpha channel based on opacity
                    alpha = (
                        background.split()[3]
                        if background.mode == "RGBA"
                        else Image.new("L", background.size, 255)
                    )
                    alpha = alpha.point(lambda p: int(p * opacity))
                    background.putalpha(alpha)

                # Get background dimensions
                bg_width, bg_height = background.size

                # Tile the background to fill the canvas (mimicking pygame's tiling behavior)
                for y in range(0, height, bg_height):
                    for x in range(0, width, bg_width):
                        canvas.paste(
                            background, (x, y), background if opacity < 1.0 else None
                        )

                return canvas
            else:
                print(f"  Warning: Background image not found: {bg_image_path}")
                # Fallback to solid color
                return Image.new("RGB", (width, height), COLORS["background"])

        except Exception as e:
            print(f"  Error loading background image: {e}")
            # Fallback to solid color
            return Image.new("RGB", (width, height), COLORS["background"])
    else:
        # No background image specified, use solid color
        bg_color = level_config.get("background_color", COLORS["background"])
        # Convert tuple if it's in the config
        if isinstance(bg_color, (list, tuple)):
            return Image.new("RGB", (width, height), tuple(bg_color))
        return Image.new("RGB", (width, height), COLORS["background"])


def render_level(level_config, output_path, show_grid=True, bg_opacity=0.3):
    """Render a single level configuration to a PNG image.

    Args:
        level_config: Level configuration dictionary
        output_path: Path to save the rendered image
        show_grid: Whether to show grid lines
        bg_opacity: Background image opacity (0.0 to 1.0, default 1.0)
    """
    try:
        # Calculate image dimensions
        min_x, min_y, width, height = calculate_level_bounds(level_config)

        # Create image with background
        image = create_background_image(level_config, width, height, bg_opacity)
        draw = ImageDraw.Draw(image, "RGBA")

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

        # Draw weapons using actual sprites
        weapon_locations = level_config.get("weapon_locations", [])
        draw_weapons_with_sprites(draw, image, weapon_locations, min_x, min_y)

        # Draw moving platforms using actual sprites (draw these before enemies)
        moving_platform_locations = level_config.get("moving_platform_locations", [])
        draw_moving_platforms_with_sprites(
            draw, image, moving_platform_locations, min_x, min_y
        )

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

        # Draw pipes using actual sprites
        pipe_locations = level_config.get("pipe_locations", [])
        if pipe_locations:
            for pipe_data in pipe_locations:
                x, y = pipe_data["x"], pipe_data["y"]
                img_x, img_y = world_to_image_coords(x, y, min_x, min_y)
                pipe_image = load_sprite_image(
                    "pipe/pipe.png", (GRIDSIZE * 2, GRIDSIZE * 2)
                )
                image.paste(pipe_image, (img_x, img_y), pipe_image)

        # Draw spikes using actual sprites
        spike_locations = level_config.get("spike_locations", [])
        if spike_locations:
            for spike_loc in spike_locations:
                if isinstance(spike_loc, tuple):
                    x, y = spike_loc
                else:
                    x, y = spike_loc["x"], spike_loc["y"]
                img_x, img_y = world_to_image_coords(x, y, min_x, min_y)
                spike_image = load_sprite_image("spike.png", (GRIDSIZE, GRIDSIZE))
                image.paste(spike_image, (img_x, img_y), spike_image)

        # Draw ladders using actual sprites
        ladder_locations = level_config.get("ladder_locations", [])
        draw_ladders_with_sprites(draw, image, ladder_locations, min_x, min_y)

        # Draw waterfalls using actual sprites
        waterfall_locations = level_config.get("waterfall_locations", [])
        draw_waterfalls_with_sprites(draw, image, waterfall_locations, min_x, min_y)

        # Draw player start position using actual sprites
        player_start = [(5, 1)]  # From PLAYER_START_X, PLAYER_START_Y in settings
        draw_special_locations_with_sprites(
            draw,
            image,
            player_start,
            min_x,
            min_y,
            "player/suffi.png",
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
        ("Weapons", COLORS["weapon"]),
        ("Enemies", COLORS["enemy"]),
        ("M.Platforms", COLORS["moving_platform"]),
        ("Pipes", COLORS["pipe"]),
        ("Spikes", COLORS["spike"]),
        ("Ladders", COLORS["ladder"]),
        ("Waterfalls", COLORS["waterfall"]),
        ("Exit", COLORS["exit"]),
        ("Player", COLORS["player_start"]),
    ]

    legend_x = 10
    legend_y = height - 20 - len(legend_items) * 15

    # Background for legend
    legend_width = 110
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
    weapon_count = len(level_config.get("weapon_locations", []))
    moving_platform_count = len(level_config.get("moving_platform_locations", []))
    pipe_count = len(level_config.get("pipe_locations", []))
    spike_count = len(level_config.get("spike_locations", []))
    ladder_count = len(level_config.get("ladder_locations", []))
    waterfall_count = len(level_config.get("waterfall_locations", []))

    info_lines = [
        f"Gems: {gem_count}",
        f"Trophies: {trophy_count}",
        f"Enemies: {enemy_count}",
        f"Powerups: {powerup_count}",
        f"Weapons: {weapon_count}",
        f"M.Platforms: {moving_platform_count}",
        f"Pipes: {pipe_count}",
        f"Spikes: {spike_count}",
        f"Ladders: {ladder_count}",
        f"Waterfalls: {waterfall_count}",
    ]

    # Position in top-right
    info_width = 140
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
        colors = [
            COLORS["gem"],
            COLORS["trophy"],
            COLORS["enemy"],
            COLORS["powerup"],
            COLORS["weapon"],
            COLORS["moving_platform"],
            COLORS["pipe"],
            COLORS["spike"],
            COLORS["ladder"],
            COLORS["waterfall"],
        ]
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
        default="platformer/assets/renders",
        help="Output directory for rendered images",
    )
    parser.add_argument(
        "--bg-opacity",
        type=float,
        default=0.3,
        help="Background image opacity (0.0 to 1.0, default 1.0)",
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
        if render_level(
            level_config,
            output_path,
            show_grid=not args.no_grid,
            bg_opacity=args.bg_opacity,
        ):
            successful_renders += 1

    print(
        f"\nRendering complete! {successful_renders}/{len(level_files)} levels rendered successfully."
    )
    print(f"Output images saved in '{args.output_dir}/' directory.")


if __name__ == "__main__":
    main()

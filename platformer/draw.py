import pygame as pg
import os
from .settings import IMAGEPATH, GRIDSIZE
from .weapon_stats import WEAPON_CONFIG


def draw_gems(screen, player):
    # Load the heart image
    try:
        heart_image = pg.image.load("platformer/data/images/heart_02.png")
        # Scale the heart to a reasonable size (adjust as needed)
        heart_image = pg.transform.scale(heart_image, (30, 30))
    except pg.error:
        # Fallback to text if image can't be loaded
        font = pg.font.Font(None, 36)
        text = font.render(f"Lives: {player.gems}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        return

    # Draw hearts for each life
    heart_spacing = 35  # Space between hearts
    start_x = 10
    start_y = 10

    for i in range(player.gems):
        x_pos = start_x + (i * heart_spacing)
        screen.blit(heart_image, (x_pos, start_y))


def draw_trophies(
    screen, player, total_trophies, trophy_image_path="data/images/trophy.png"
):
    # Load the trophy image
    try:
        trophy_image = pg.image.load(f"platformer/{trophy_image_path}")
        # Scale the trophy to a reasonable size (adjust as needed)
        trophy_image = pg.transform.scale(trophy_image, (25, 25))
    except pg.error:
        # Fallback to text if image can't be loaded
        font = pg.font.Font(None, 36)
        text = font.render(
            f"Trophies: {player.trophies_collected} / {total_trophies}",
            True,
            (255, 255, 255),
        )
        screen.blit(text, (10, 50))
        return

    # Draw trophies
    trophy_spacing = 30  # Space between trophies
    start_x = 10
    start_y = 50

    # Draw collected trophies (full color)
    for i in range(player.trophies_collected):
        x_pos = start_x + (i * trophy_spacing)
        screen.blit(trophy_image, (x_pos, start_y))

    # Draw uncollected trophies (grayed out)
    for i in range(player.trophies_collected, total_trophies):
        x_pos = start_x + (i * trophy_spacing)
        # Create a grayed out version of the trophy
        gray_trophy = trophy_image.copy()
        gray_trophy.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
        screen.blit(gray_trophy, (x_pos, start_y))


def draw_health_bar(screen, player, width, height, max_health):
    bar_width = width
    bar_height = height
    bar_x = screen.get_width() - bar_width - 20
    bar_y = 10
    fill_width = int((player.health / max_health) * bar_width)
    pg.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
    pg.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))
    pg.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)


def fade_to_black(screen, draw_callback, width, height, duration=60):
    """Fade the screen to black from the center outward over 'duration' frames."""
    clock = pg.time.Clock()
    for frame in range(duration):
        draw_callback()
        max_radius = int((width**2 + height**2) ** 0.5 // 2)
        radius = int((frame / duration) * max_radius)
        fade_surface = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.circle(fade_surface, (0, 0, 0, 255), (width // 2, height // 2), radius)
        screen.blit(fade_surface, (0, 0))
        pg.display.flip()
        clock.tick(60)


def show_level_complete_text(screen, width, height):
    """Display 'Level Complete!' in big white letters at the center of the screen."""
    screen.fill((0, 0, 0))
    font = pg.font.Font(None, 120)
    text = font.render("Level Complete!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pg.display.flip()

    # Wait until user closes window or presses any key
    import sys

    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN):
                waiting = False
    pg.quit()
    sys.exit()

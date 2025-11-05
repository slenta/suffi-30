"""
Drawing utility functions for the game.

This module contains pure drawing functions that render various game elements.
These functions are stateless and can be called from anywhere with the appropriate parameters.

Functions are organized into categories:
- HUD elements: gems, trophies, health bars, score, timer
- Screen effects: fade transitions, encounter messages, Marvin mode indicator
- Background rendering: parallax scrolling background
- UI screens: level complete text (legacy)

For game state-dependent drawing orchestration, see GameWorld.draw() in gameworld.py.
"""

import pygame as pg
import os
from ..config.settings import IMAGEPATH, GRIDSIZE
from ..config.weapon_config import WEAPON_CONFIG


def draw_gems(screen, player):
    # Load the heart image
    try:
        heart_image = pg.image.load(os.path.join(IMAGEPATH, "heart_02.png"))
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


def draw_trophies(screen, player, total_trophies, trophy_image_path="trophy.png"):
    # Load the trophy image
    try:
        # trophy_image_path is relative to IMAGEPATH (assets/images/)
        trophy_image = pg.image.load(os.path.join(IMAGEPATH, trophy_image_path))
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
    bar_x = screen.get_width() - bar_width - 200
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


def draw_score(screen, score, width):
    """
    Draw the current score in the bottom right corner.

    Args:
        screen: Pygame screen surface
        score: Current score (int)
        width: Screen width
    """
    font = pg.font.Font(None, 36)
    score_text = f"Score: {score:,}"
    score_surface = font.render(score_text, True, (255, 255, 255))

    # Position in bottom right corner with some padding
    score_rect = score_surface.get_rect()
    score_rect.bottomright = (width - 20, screen.get_height() - 10)

    # Draw semi-transparent background for better readability
    bg_rect = score_rect.inflate(20, 10)
    bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
    bg_surface.fill((0, 0, 0, 128))
    screen.blit(bg_surface, bg_rect.topleft)

    # Draw the score
    screen.blit(score_surface, score_rect)


def draw_timer(screen, time_remaining, width):
    """
    Draw the countdown timer in the top right corner.

    Args:
        screen: Pygame screen surface
        time_remaining: Time remaining in seconds (float)
        width: Screen width
    """
    if time_remaining is None:
        return

    # Format time as MM:SS
    minutes = int(time_remaining // 60)
    seconds = int(time_remaining % 60)
    time_text = f"{minutes:02d}:{seconds:02d}"

    # Choose color based on remaining time
    if time_remaining <= 10:
        color = (255, 0, 0)  # Red when less than 10 seconds
    elif time_remaining <= 30:
        color = (255, 165, 0)  # Orange when less than 30 seconds
    else:
        color = (255, 255, 255)  # White otherwise

    # Render the timer text
    font = pg.font.Font(None, 48)
    timer_surface = font.render(time_text, True, color)

    # Position in top right corner with some padding
    timer_rect = timer_surface.get_rect()
    timer_rect.topright = (width - 20, 10)

    # Draw semi-transparent background for better readability
    bg_rect = timer_rect.inflate(20, 10)
    bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
    bg_surface.fill((0, 0, 0, 128))
    screen.blit(bg_surface, bg_rect.topleft)

    # Draw the timer
    screen.blit(timer_surface, timer_rect)


def draw_encounter_message(screen, message, width, height):
    """
    Draw an encounter message in yellow at the center of the screen.

    Args:
        screen: Pygame screen surface
        message: Message text to display
        width: Screen width
        height: Screen height
    """
    if not message:
        return

    # Render the message in yellow
    font = pg.font.Font(None, 36)
    message_surface = font.render(message, True, (255, 255, 0))

    # Position at center of screen
    message_rect = message_surface.get_rect()
    message_rect.center = (width // 2, height // 2)

    # Draw semi-transparent black background for better readability
    bg_rect = message_rect.inflate(40, 20)
    bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
    bg_surface.fill((0, 0, 0, 180))
    screen.blit(bg_surface, bg_rect.topleft)

    # Draw the message
    screen.blit(message_surface, message_rect)


def draw_marvin_mode(screen, width):
    """
    Draw the Marvin Mode indicator (MFG) at the top center.

    Args:
        screen: Pygame screen surface
        width: Screen width
    """
    font = pg.font.Font(None, 72)
    marvin_text = font.render("MFG", True, (255, 215, 0))  # Gold color
    text_rect = marvin_text.get_rect(center=(width // 2, 40))

    # Add a semi-transparent black background for better readability
    bg_rect = text_rect.inflate(20, 10)
    bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
    bg_surface.fill((0, 0, 0, 128))
    screen.blit(bg_surface, bg_rect.topleft)
    screen.blit(marvin_text, text_rect)


def draw_background(
    screen,
    background_image,
    background_scroll_speed,
    camera_offset_x,
    camera_offset_y,
    background_color=(135, 206, 235),
):
    """
    Draw the background - either an image or solid color.
    Tiles the background at its original size with parallax scrolling.

    Args:
        screen: Pygame screen surface
        background_image: Pygame surface of the background image (None for solid color)
        background_scroll_speed: Parallax scroll speed multiplier
        camera_offset_x: Camera X offset
        camera_offset_y: Camera Y offset
        background_color: RGB tuple for solid color fallback
    """
    if background_image:
        # Calculate parallax scrolling offset for both X and Y
        bg_offset_x = int(camera_offset_x * background_scroll_speed)
        bg_offset_y = int(camera_offset_y * background_scroll_speed)

        # Get background and screen dimensions
        bg_width = background_image.get_width()
        bg_height = background_image.get_height()
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Tile the background at its original size (no scaling)
        # The offset is applied through the modulo to create seamless scrolling
        start_x = -(bg_offset_x % bg_width) if bg_width > 0 else 0
        start_y = -(bg_offset_y % bg_height) if bg_height > 0 else 0

        # Draw background tiles
        y = start_y
        while y < screen_height:
            x = start_x
            while x < screen_width:
                screen.blit(background_image, (x, y))
                x += bg_width
            y += bg_height
    else:
        # Fall back to solid color background
        screen.fill(background_color)

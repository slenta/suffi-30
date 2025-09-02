import pygame as pg


def draw_gems(screen, player):
    font = pg.font.Font(None, 36)
    text = font.render(f"Player Lives: {player.gems}", True, (255, 255, 255))
    screen.blit(text, (10, 10))


def draw_trophies(screen, player, total_trophies):
    font = pg.font.Font(None, 36)
    text = font.render(
        f"Trophies Collected: {player.trophies_collected} / {total_trophies}",
        True,
        (255, 255, 255),
    )
    screen.blit(text, (10, 50))


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
    """Fade the screen to black from the center outward over 'duration' frames.
    draw_callback: function to draw the current game frame (e.g. GameWorld.draw)
    """
    clock = pg.time.Clock()
    for frame in range(duration):
        draw_callback()  # Draw the current frame
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

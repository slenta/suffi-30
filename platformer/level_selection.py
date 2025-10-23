"""
Level Selection Screen

Mario-style level selection screen where players can choose levels using arrow keys.
"""

import asyncio
import pygame as pg
import os
from .settings import *
from .sound_manager import sound_manager


class LevelSelectionScreen:
    """Mario-style level selection screen."""

    def __init__(self, screen):
        self.screen = screen
        self.font_large = pg.font.Font(None, 64)
        self.font_medium = pg.font.Font(None, 32)
        self.font_small = pg.font.Font(None, 16)

        # Get available levels
        self.available_levels = self.get_available_levels()
        self.selected_level_index = 0
        self.selected_level = (
            self.available_levels[0] if self.available_levels else "level1"
        )

        # Colors
        self.bg_color = (128, 0, 128)  # Dark blue
        self.title_color = (255, 255, 255)  # White
        self.level_color = (200, 200, 200)  # Light gray
        self.selected_color = (255, 255, 0)  # Yellow
        self.cursor_color = (255, 100, 100)  # Red

        # Animation
        self.cursor_blink_timer = 0
        self.cursor_visible = True

        print(
            f"🎮 Level Selection Screen initialized with {len(self.available_levels)} levels"
        )

    def get_available_levels(self):
        """Get list of available levels from the levels directory (excluding sub-levels)."""
        levels_dir = os.path.join(os.path.dirname(__file__), "levels")
        available_levels = []

        try:
            for file in os.listdir(levels_dir):
                if file.endswith(".py") and file != "__init__.py":
                    level_name = file[:-3]  # Remove .py extension
                    # Skip sub-levels (those ending with "-sub")
                    if not level_name.endswith("-sub"):
                        available_levels.append(level_name)
        except FileNotFoundError:
            print("❌ Levels directory not found")
            return ["level1"]  # Fallback

        return sorted(available_levels)

    def get_level_display_name(self, level_name):
        """Convert level filename to display name."""
        # Convert level1-advanced to "Level 1 - Advanced"
        display_name = level_name.replace("level", "Level ").replace("-", " - ")
        return display_name.title()

    def handle_input(self, event):
        """Handle keyboard input for level selection."""
        if event.type == pg.KEYDOWN:
            if event.key == KEYBINDINGS.get("left") or event.key == pg.K_UP:
                # Move selection up
                self.selected_level_index = (self.selected_level_index - 1) % len(
                    self.available_levels
                )
                self.selected_level = self.available_levels[self.selected_level_index]
                sound_manager.play_sound_effect("menu_move")
                return None

            elif event.key == KEYBINDINGS.get("right") or event.key == pg.K_DOWN:
                # Move selection down
                self.selected_level_index = (self.selected_level_index + 1) % len(
                    self.available_levels
                )
                self.selected_level = self.available_levels[self.selected_level_index]
                sound_manager.play_sound_effect("menu_move")
                return None

            elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                # Select current level
                sound_manager.play_sound_effect("menu_select")
                print(f"🎯 Selected level: {self.selected_level}")
                return self.selected_level

            elif event.key == KEYBINDINGS.get("quit"):
                # Quit game
                return "QUIT"

        return None

    def update(self):
        """Update screen animations."""
        # Cursor blinking animation
        self.cursor_blink_timer += 1
        if self.cursor_blink_timer >= 30:  # Blink every 0.5 seconds at 60 FPS
            self.cursor_visible = not self.cursor_visible
            self.cursor_blink_timer = 0

    def draw(self):
        """Draw the level selection screen."""
        # Clear screen with background color
        self.screen.fill(self.bg_color)

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Draw title
        title_text = self.font_large.render("SUFFI ON THE RUN", True, self.title_color)
        title_rect = title_text.get_rect(center=(screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Draw level list
        start_y = 100
        level_spacing = 30

        for i, level_name in enumerate(self.available_levels):
            y_pos = start_y + (i * level_spacing)

            # Determine colors for this level
            if i == self.selected_level_index:
                text_color = self.selected_color
            else:
                text_color = self.level_color

            # Draw level name (same font size for all levels)
            display_name = self.get_level_display_name(level_name)
            level_text = self.font_medium.render(display_name, True, text_color)
            level_rect = level_text.get_rect(center=(screen_width // 2, y_pos))
            self.screen.blit(level_text, level_rect)

            # Draw selection cursor
            if i == self.selected_level_index and self.cursor_visible:
                cursor_x = level_rect.left - 30
                cursor_y = y_pos
                cursor_text = self.font_medium.render("►", True, self.cursor_color)
                cursor_rect = cursor_text.get_rect(center=(cursor_x, cursor_y))
                self.screen.blit(cursor_text, cursor_rect)

        # Update display
        pg.display.flip()

    async def run(self):
        """Run the level selection screen loop (async for web compatibility)."""
        clock = pg.time.Clock()
        running = True

        while running:
            clock.tick(FPS)

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "QUIT"

                result = self.handle_input(event)
                if result is not None:
                    return result

            # Update and draw
            self.update()
            self.draw()

            # Yield control to allow async operations (critical for web)
            await asyncio.sleep(0)

        return self.selected_level

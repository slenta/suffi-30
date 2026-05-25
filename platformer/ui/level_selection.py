"""
Level Selection Screen

Mario-style level selection screen where players can choose levels using arrow keys.
"""

import asyncio
import pygame as pg
import os
from ..config.settings import *
from ..config.api_config import API_BASE_URL
from ..core.highscore_manager import HighscoreManager
from ..core.sound_manager import sound_manager
from .highscore_screen import HighscoreScreen
from .instructions_screen import InstructionsScreen


HIGHSCORES_ENTRY = "__highscores__"
INSTRUCTIONS_ENTRY = "__instructions__"
SPECIAL_ENTRIES = (HIGHSCORES_ENTRY, INSTRUCTIONS_ENTRY)


class LevelSelectionScreen:
    """Mario-style level selection screen."""

    def __init__(self, screen):
        self.screen = screen
        self.font_large = pg.font.Font(TITLE_FONT, 28)
        # Load Ketchum font for level names
        ketchum_font_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "fonts",
            "Ketchum.otf",
        )
        self.font_medium = pg.font.Font(ketchum_font_path, 22)
        self.font_small = pg.font.Font(ketchum_font_path, 16)

        # Get available levels and append the special menu entries (below a divider)
        self.available_levels = self.get_available_levels()
        self.menu_items = self.available_levels + [HIGHSCORES_ENTRY, INSTRUCTIONS_ENTRY]
        self.selected_level_index = 0
        self.selected_level = self.menu_items[0]
        self.highscore_manager = HighscoreManager(api_base_url=API_BASE_URL)

        # Colors
        self.bg_color = (128, 0, 128)
        # self.title_color = (1, 255, 245)
        self.title_color = (255, 195, 0)
        self.level_color = (200, 200, 200)
        self.selected_color = (255, 195, 0)
        self.highscore_color = (100, 220, 200)
        self.cursor_color = self.selected_color

        # Animation
        self.cursor_blink_timer = 0
        self.cursor_visible = True

        # Load player sprite for cursor
        player_sprite_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "images",
            "player",
            "suffi.png",
        )
        try:
            self.cursor_sprite = pg.image.load(player_sprite_path).convert_alpha()
            # Scale sprite to match the smaller menu font
            self.cursor_sprite = pg.transform.scale(self.cursor_sprite, (24, 24))
        except FileNotFoundError:
            print(f"❌ Player sprite not found at {player_sprite_path}")
            self.cursor_sprite = None

        # Load player sprite for bottom animation (running across screen)
        try:
            self.running_sprite = pg.image.load(player_sprite_path).convert_alpha()
            # Scale sprite for bottom animation (bigger than cursor)
            self.running_sprite = pg.transform.scale(self.running_sprite, (24, 24))
        except FileNotFoundError:
            print(f"❌ Running sprite not found at {player_sprite_path}")
            self.running_sprite = None

        # Animation variables for running sprite
        self.running_sprite_x = -60  # Start off-screen to the left
        self.running_sprite_speed = 2  # Pixels per frame
        self.screen_width = screen.get_width()

        print(
            f"🎮 Level Selection Screen initialized with {len(self.available_levels)} levels"
        )

        # Start menu music
        menu_music_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "music", "menu.ogg"
        )
        sound_manager.play_background_music(menu_music_path, loop=True)

    def get_available_levels(self):
        """Get list of available levels from the levels directory (excluding sub-levels)."""
        # Go up one level from ui/ to platformer/, then into levels/
        levels_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "levels")
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
        if level_name == HIGHSCORES_ENTRY:
            return "HIGHSCORES"
        if level_name == INSTRUCTIONS_ENTRY:
            return "INSTRUCTIONS"
        # Convert level1-advanced to "Level 1 - Advanced"
        display_name = level_name.replace("level", "Level ").replace("-", " - ")
        return display_name.title().upper()

    def handle_input(self, event):
        """Handle keyboard input for level selection."""
        if event.type == pg.KEYDOWN:
            if event.key == KEYBINDINGS.get("left") or event.key == pg.K_UP:
                # Move selection up
                self.selected_level_index = (self.selected_level_index - 1) % len(
                    self.menu_items
                )
                self.selected_level = self.menu_items[self.selected_level_index]
                sound_manager.play_sound_effect("menu_move")
                return None

            elif event.key == KEYBINDINGS.get("right") or event.key == pg.K_DOWN:
                # Move selection down
                self.selected_level_index = (self.selected_level_index + 1) % len(
                    self.menu_items
                )
                self.selected_level = self.menu_items[self.selected_level_index]
                sound_manager.play_sound_effect("menu_move")
                return None

            elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                # Select current level. Lighter blip for info overlays;
                # committing to a real level keeps the heavier confirm sound.
                if self.selected_level in SPECIAL_ENTRIES:
                    sound_manager.play_sound_effect("menu_move")
                else:
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

        # Update running sprite position
        self.running_sprite_x += self.running_sprite_speed

        # Reset position when sprite goes off-screen to the right
        if self.running_sprite_x > self.screen_width + 60:
            self.running_sprite_x = -60

    def draw(self):
        """Draw the level selection screen."""
        # Clear screen with background color
        self.screen.fill(self.bg_color)

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Draw title (smaller now to free vertical space)
        title_text = self.font_large.render("SUFFI ON THE RUN", True, self.title_color)
        title_rect = title_text.get_rect(center=(screen_width // 2, 28))
        self.screen.blit(title_text, title_rect)

        # Draw menu: levels first, then a divider, then the special entries
        start_y = 64
        level_spacing = 26
        special_offset = 18  # extra gap before the special-entries block

        for i, level_name in enumerate(self.menu_items):
            is_special = level_name in SPECIAL_ENTRIES
            is_selected = i == self.selected_level_index

            y_pos = start_y + (i * level_spacing)
            if is_special:
                y_pos += special_offset

            if is_selected:
                text_color = self.selected_color
            elif is_special:
                text_color = self.highscore_color
            else:
                text_color = self.level_color

            display_name = self.get_level_display_name(level_name)
            level_text = self.font_medium.render(display_name, True, text_color)
            level_rect = level_text.get_rect(center=(screen_width // 2, y_pos))
            self.screen.blit(level_text, level_rect)

            if is_selected and self.cursor_visible:
                cursor_x = level_rect.left - 36
                cursor_y = y_pos
                if self.cursor_sprite:
                    cursor_rect = self.cursor_sprite.get_rect(
                        center=(cursor_x, cursor_y)
                    )
                    self.screen.blit(self.cursor_sprite, cursor_rect)
                else:
                    cursor_text = self.font_medium.render("►", True, self.cursor_color)
                    cursor_rect = cursor_text.get_rect(center=(cursor_x, cursor_y))
                    self.screen.blit(cursor_text, cursor_rect)

        # Draw running sprite at the bottom of the screen
        if self.running_sprite:
            running_sprite_y = screen_height - 20  # Position near bottom
            running_sprite_rect = self.running_sprite.get_rect(
                center=(self.running_sprite_x, running_sprite_y)
            )
            self.screen.blit(self.running_sprite, running_sprite_rect)

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
                    # Stop menu music before quitting
                    sound_manager.stop_music()
                    return "QUIT"

                result = self.handle_input(event)
                if result in SPECIAL_ENTRIES:
                    # Show overlay screen; stay in selection loop afterwards
                    if result == HIGHSCORES_ENTRY:
                        overlay = HighscoreScreen(
                            self.screen, self.highscore_manager
                        )
                    else:
                        overlay = InstructionsScreen(self.screen)
                    overlay_result = await overlay.run()
                    if overlay_result == "QUIT":
                        sound_manager.stop_music()
                        return "QUIT"
                    pg.event.clear()
                    continue
                if result is not None:
                    # Stop menu music before returning
                    sound_manager.stop_music()
                    return result

            # Update and draw
            self.update()
            self.draw()

            # Yield control to allow async operations (critical for web)
            await asyncio.sleep(0)

        return self.selected_level

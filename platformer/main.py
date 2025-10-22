import asyncio
import os
import sys
import pygame as pg
from .gameworld import GameWorld
from .level_selection import LevelSelectionScreen
from .settings import FPS, KEYBINDINGS, WIDTH, HEIGHT


def get_level_to_load():
    """Get the level to load from environment variable or show level selection."""
    # Check if level was specified via command line (for backwards compatibility)
    level_name = os.environ.get("PLATFORMER_LEVEL")
    if level_name:
        print(f"🎯 Loading level from command line: {level_name}")
        return level_name

    # Show level selection screen
    print("🎮 Starting level selection screen...")
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Level Selection - Suffi Platformer")

    # Load menu sound effects
    from .sound_manager import sound_manager

    sound_manager.load_sound_effect("menu_move", "assets/sounds/menu_move.wav")
    sound_manager.load_sound_effect("menu_select", "assets/sounds/menu_select.wav")

    level_selection = LevelSelectionScreen(screen)
    selected_level = level_selection.run()

    if selected_level == "QUIT":
        print("👋 Player quit from level selection")
        pg.quit()
        sys.exit()

    print(f"🎯 Selected level: {selected_level}")
    return selected_level


# Initialize the game world
world = GameWorld()
world.load_level(get_level_to_load())  # Load selected level configuration
world.start_screen()


# Main game loop
async def main():
    running = True
    while running and world.keep_going:
        world.clock.tick(world.current_fps)
        world.events()  # All event handling happens here
        world.update()
        world.draw()
        await asyncio.sleep(0)  # Ensures smooth async operation


# Run the game
asyncio.run(main())

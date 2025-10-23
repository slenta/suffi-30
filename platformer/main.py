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
        # Clear the environment variable so next time we show level selection
        del os.environ["PLATFORMER_LEVEL"]
        return level_name

    # Show level selection screen
    print("🎮 Starting level selection screen...")
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Level Selection - Suffi Platformer")

    # Load menu sound effects
    from .sound_manager import sound_manager

    sounds_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "assets", "sounds"
    )
    sound_manager.load_sound_effect(
        "menu_move", os.path.join(sounds_dir, "menu_move.wav")
    )
    sound_manager.load_sound_effect(
        "menu_select", os.path.join(sounds_dir, "menu_select.wav")
    )

    level_selection = LevelSelectionScreen(screen)
    selected_level = level_selection.run()

    if selected_level == "QUIT":
        print("👋 Player quit from level selection")
        pg.quit()
        sys.exit()

    print(f"🎯 Selected level: {selected_level}")
    return selected_level


# Main game loop
async def main():
    # Main game loop - allows returning to level selection after completing a level
    while True:
        # Initialize the game world
        world = GameWorld()
        world.load_level(get_level_to_load())  # Load selected level configuration
        world.start_screen()

        # Run the level
        running = True
        while running and world.keep_going:
            world.clock.tick(world.current_fps)
            world.events()  # All event handling happens here
            world.update()
            world.draw()
            await asyncio.sleep(0)  # Ensures smooth async operation

        # Check if we should return to level selection or quit
        print(
            f"🔍 DEBUG: return_to_level_selection = {world.return_to_level_selection}"
        )
        print(f"🔍 DEBUG: keep_going = {world.keep_going}")
        if world.return_to_level_selection:
            print("🔄 Returning to level selection...")
            continue  # Go back to level selection
        else:
            # Player quit the game
            print("👋 Exiting game...")
            break

    # Clean up and exit
    pg.quit()
    sys.exit()


# Run the game
asyncio.run(main())

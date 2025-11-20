import asyncio
import os
import sys
import pygame as pg

# Use absolute imports for Pygbag compatibility
try:
    # Try relative imports first (for local development)
    from .core.gameworld import GameWorld
    from .ui.level_selection import LevelSelectionScreen
    from .config.settings import FPS, KEYBINDINGS, WIDTH, HEIGHT
except ImportError:
    # Fall back to absolute imports (for Pygbag)
    from core.gameworld import GameWorld
    from ui.level_selection import LevelSelectionScreen
    from config.settings import FPS, KEYBINDINGS, WIDTH, HEIGHT


async def get_level_to_load():
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
    # Only init pygame if not already initialized (Pygbag handles this)
    if not pg.get_init():
        pg.init()

    # Wait for display to be ready (important for pygbag)
    screen = pg.display.get_surface()
    retry_count = 0
    while screen is None and retry_count < 10:
        await asyncio.sleep(0.1)  # Wait for pygbag to initialize display
        screen = pg.display.get_surface()
        retry_count += 1

    if screen is None:
        print("⚠️ Display not ready from pygbag, creating new surface")
        screen = pg.display.set_mode((WIDTH, HEIGHT))

    pg.display.set_caption("Level Selection - Suffi Platformer")

    # Load menu sound effects
    try:
        from .core.sound_manager import sound_manager
    except ImportError:
        from core.sound_manager import sound_manager

    sounds_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "assets", "sounds"
    )
    menu_move_sound = sound_manager.load_sound_effect(
        "menu_move", os.path.join(sounds_dir, "menu_move.ogg")
    )
    menu_select_sound = sound_manager.load_sound_effect(
        "menu_select", os.path.join(sounds_dir, "menu_select.ogg")
    )

    # Boost menu sound volumes since they're naturally quiet
    if menu_move_sound:
        menu_move_sound.set_volume(1.5)  # 150% volume
    if menu_select_sound:
        menu_select_sound.set_volume(1.5)  # 150% volume

    level_selection = LevelSelectionScreen(screen)
    selected_level = await level_selection.run()  # Now async!

    if selected_level == "QUIT":
        print("👋 Player quit from level selection")
        pg.quit()
        sys.exit()

    print(f"🎯 Selected level: {selected_level}")
    return selected_level


# Main game loop
async def main():
    print("🎮 Starting main game loop...")

    # Ensure pygame is initialized (important for pygbag)
    if not pg.get_init():
        pg.init()

    # Wait for display to be ready in pygbag environment
    if sys.platform == "emscripten":
        print("🌐 Detected pygbag/emscripten environment, waiting for display...")
        retry_count = 0
        while pg.display.get_surface() is None and retry_count < 20:
            await asyncio.sleep(0.1)
            retry_count += 1
        print(f"✅ Display ready after {retry_count} retries")

    # Main game loop - allows returning to level selection after completing a level
    while True:
        # Initialize the game world
        world = GameWorld()
        selected_level = await get_level_to_load()  # Now async!
        world.load_level(selected_level)  # Load selected level configuration
        world.start_screen()

        # Run the level
        running = True
        while running and world.keep_going:
            world.clock.tick(world.current_fps)
            world.events()  # All event handling happens here
            world.update()
            world.draw()

            # Check for level completion (needs to be async)
            if world.level_complete_flag:
                world.level_complete_flag = False  # Reset flag
                await world.level_complete()

            # Check for game over (needs to be async)
            if world.game_over_flag:
                world.game_over_flag = False  # Reset flag
                await world.game_over()

            await asyncio.sleep(
                0
            )  # Ensures smooth async operation        # Check if we should return to level selection or quit
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


# Run the game when executed directly
if __name__ == "__main__":
    asyncio.run(main())

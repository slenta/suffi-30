import asyncio
import os
import pygame as pg
from .gameworld import GameWorld
from .settings import FPS, KEYBINDINGS


def get_level_to_load():
    """Get the level to load from environment variable or use default."""
    level_name = os.environ.get('PLATFORMER_LEVEL', 'level1')
    print(f"🎯 Loading level: {level_name}")
    return level_name


# Initialize the game world
world = GameWorld()
world.load_level(get_level_to_load())  # Load selected level configuration
world.start_screen()


# Main game loop
async def main():
    running = True
    while running and world.keep_going:
        world.clock.tick(FPS)
        world.events()
        world.update()
        world.draw()
        await asyncio.sleep(0)  # Ensures smooth async operation
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                # Keep handling minimal here; specific actions are handled in GameWorld.events()
                if event.key == KEYBINDINGS.get("throw"):
                    world.player.throw_exploding_object()


# Run the game
asyncio.run(main())

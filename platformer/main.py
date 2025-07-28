import asyncio
from .gameworld import GameWorld
from .settings import FPS

# Initialize the game world
world = GameWorld()
world.load_level("level1")  # Load level1 configuration
world.start_screen()


# Main game loop
async def main():
    while world.keep_going:
        world.clock.tick(FPS)
        world.events()
        world.update()
        world.draw()
        await asyncio.sleep(0)  # Ensures smooth async operation


# Run the game
asyncio.run(main())

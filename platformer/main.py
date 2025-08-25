import asyncio
import pygame as pg
from .gameworld import GameWorld
from .settings import FPS

# Initialize the game world
world = GameWorld()
world.load_level("level1")  # Load level1 configuration
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
                if event.key == pg.K_e:  # Check if the 'E' key is pressed
                    world.player.throw_exploding_object()


# Run the game
asyncio.run(main())

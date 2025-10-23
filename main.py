#!/usr/bin/env python3
"""
Main entry point for pygbag web deployment.
This file must be in the root directory for pygbag to work.
"""

import asyncio
import sys
import os

# Ensure the platformer package can be imported
sys.path.insert(0, os.path.dirname(__file__))


async def main():
    """Main entry point for the game."""
    from platformer.main import main as game_main

    await game_main()


if __name__ == "__main__":
    asyncio.run(main())

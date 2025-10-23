#!/usr/bin/env python3
"""
Simple entry point for the platformer game.
For local development convenience - runs platformer.main directly
"""

if __name__ == "__main__":
    import asyncio
    from platformer.main import main

    asyncio.run(main())

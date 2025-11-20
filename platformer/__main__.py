"""
Entry point for the Suffi Platformer game.
This file is used when running the package with `python -m platformer`
or when building with Pygbag.
"""

import asyncio
from .main import main

# For Pygbag compatibility
asyncio.run(main())

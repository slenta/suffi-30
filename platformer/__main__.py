"""
Entry point when running as: python -m platformer
This is only used for local development, not for Pygbag.
"""

import asyncio
from .main import main

# Local development only
asyncio.run(main())

import asyncio
import sys
from platformer.main import main

if __name__ == "__main__":
    if sys.platform == "emscripten":
        asyncio.ensure_future(main())
    else:
        asyncio.run(main())

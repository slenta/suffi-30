import asyncio
import sys
from platformer.main import main

# For pygbag: when this module is run, __name__ will be "__main__"
# but we need to handle async properly
if __name__ == "__main__":
    asyncio.run(main())

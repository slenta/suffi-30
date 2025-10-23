# suffi-30
level up through suffisuffzich's life by playing this simple jump n run game

## How to Play

### Quick start (local development):
```bash
python play.py                    # Show level selection screen
python play.py level2             # Play level2 directly
python play.py --list-levels      # List all available levels
```

## Web Deployment with Pygbag

This game can be deployed to the web using [pygbag](https://github.com/pygame-web/pygbag), which converts Pygame applications to run in the browser using WebAssembly.

### Prerequisites
```bash
pip install pygbag
```

### Local Testing
Test the web version locally before deploying:
```bash
# This builds and serves the game on http://localhost:8000
python -m pygbag --PYBUILD 3.12 --disable-sound-format-error .
```

Then open your browser to `http://localhost:8000` to play the web version.

### Building for Deployment
To build the web version without running the server:
```bash
# Build only (output will be in build/web/)
python -m pygbag --build --PYBUILD 3.12 --disable-sound-format-error .
```

The built files will be in `build/web/`. You can deploy these files to any static hosting service (GitHub Pages, Netlify, etc.).

### Deployment Options

#### Option 1: GitHub Pages (itch.io style)
1. Build the game with `--build` flag
2. Upload the `build/web/` contents to your GitHub Pages repository
3. The game will be accessible at `https://yourusername.github.io/repository-name/`

#### Option 2: Itch.io
1. Build with: `python -m pygbag --build --itch --PYBUILD 3.12 --disable-sound-format-error .`
2. Create a ZIP of the `build/web/` directory
3. Upload to itch.io as an HTML5 game

### Notes
- The `--disable-sound-format-error` flag is needed because some sound files may not be in the optimal format for web
- The `--PYBUILD 3.12` specifies the Python version to use in the web build
- The game includes a level selection screen that works in both desktop and web versions


# ToDo-Liste
- gameworld etwas höher gestalten
- modify player image, strength, speed to level
- add weapons, which can be used when collected (Spraydose, Milchflasche etc.) -> was machen die?
- add End to Level --> Trophy collection, when coming to end with all trophys end level
- level name/description am anfang einblenden 
- level ideas:
    - im club
    - im krankenhaus
    - im kindergarten
    - im schule
    - pubertät --> ziel an mama und papa vorbeizuschleichen
    - krankenhaus
- Highscore wäre nice
- check web deployment
- python files aufräumen
- consistent assets management (filepaths, clean up file system)
- more enemy mechanics (police with light)
- spray can paint the walls with a score?
- schalter
- haunted house ghosts police lights
- mehrere ebenen und display bewegt sich mit
- durchn tisch treten als pipes mit animation
- launcher screen mit level auswahl nicht nur mit pfeiltasten
- graffiti malen

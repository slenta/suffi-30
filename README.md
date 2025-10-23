# suffi-30
level up through suffisuffzich's life by playing this simple jump n run game

# Quick start (local development):
```bash
python play.py                    # Show level selection screen
python play.py trancefloor             # Play level trancefloor directly
python play.py --list-levels      # List all available levels
```

# Web Deployment with Pygbag

This game can be deployed to the web using [pygbag](https://github.com/pygame-web/pygbag), which converts Pygame applications to run in the browser using WebAssembly.

## Prerequisites
```bash
pip install pygbag
```

## Local Deployment
Test the web version locally before deploying:
```bash
# This builds and serves the game on http://localhost:8000
python -m pygbag --PYBUILD 3.12 --disable-sound-format-error .
```

Then open your browser to `http://localhost:8000` to play the web version.

- The `--disable-sound-format-error` flag is needed because some sound files may not be in the optimal format for web


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
- convert all mp3 to ogg

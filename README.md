# suffi-30
level up through suffisuffzich's life by playing this simple jump n run game

## Play local:

```bash
python play.py                    # Show level selection screen
python play.py trancefloor        # Play level trancefloor directly
python play.py --list-levels      # List all available levels
```

## Play local in browser on `http://localhost:8000`

```bash
# This builds and serves the game on http://localhost:8000
python -m pygbag --PYBUILD 3.12 .
# This builds and serves the game with a custom template on http://localhost:8000
python -m pygbag --PYBUILD 3.12 --template custom.tmpl .
python -m pygbag --PYBUILD 3.12 --build --template custom.tmpl .
```

## Play online via vercel

### Prerequisites
* Login to Vercel: `vercel login`
* Deploy: `vercel --prod`


# ToDo-Liste
- modify player image, strength, speed to level
- add weapons, which can be used when collected (Spraydose, Milchflasche etc.) -> was machen die?
- level name/description am anfang einblenden 
- level ideas:
    - im club
    - im krankenhaus
    - im kindergarten
    - im schule
    - pubertät --> ziel an mama und papa vorbeizuschleichen
    - krankenhaus
- python files aufräumen
- consistent assets management (filepaths, clean up file system)
- more enemy mechanics (police with light)
- spray can paint the walls with a score?
- schalter
- haunted house ghosts police lights
- graffiti malen


ideas trancefloor:
- sub level at the bar
- background
- the final enemy is yourself
- plh



apfel
brotschnitte
bier
discokugel
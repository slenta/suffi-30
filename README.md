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
python -m pygbag --PYBUILD 3.12 .
```

Then open your browser to `http://localhost:8000` to play the web version.

## Vercel Deployment

Deploy to Vercel for production hosting with highscore API:

### Prerequisites
1. Install Vercel CLI: `npm install -g vercel`
2. Create a [Vercel account](https://vercel.com)

### Deployment Steps

1. **Login to Vercel:**
```bash
vercel login
```

2. **Deploy:**
```bash
vercel
```

Follow the prompts:
- Set up and deploy? `Y`
- Which scope? Choose your account
- Link to existing project? `N` (first time)
- Project name: `suffi-30`
- In which directory is your code located? `./`

3. **Production deployment:**
```bash
vercel --prod
```

### Highscore API

The project includes a serverless API for highscores at `/api/highscores`:

**Get highscores:**
```bash
GET /api/highscores
```

**Submit highscore:**
```bash
POST /api/highscores
Content-Type: application/json

{
  "name": "PlayerName",
  "score": 1000,
  "level": "trancefloor"
}
```

### Optional: Add Database

For persistent highscore storage, add Vercel Postgres or KV:

```bash
# Install Vercel Postgres
vercel link
vercel env pull .env.local
```

Then uncomment the database code in `api/highscores.py`.

### GitHub Integration

For automatic deployments on push:
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Vercel will auto-deploy on every push to main

# ToDo-Liste
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


ideas trancefloor:
- dj enemy (in dj booth)
- sub level at the bar
- background
- the final enemy is yourself
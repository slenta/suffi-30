# suffi-30
level up through suffisuffzich's life by playing this simple jump n run game

## Quick start (local development):
```bash
python play.py                    # Show level selection screen
python play.py trancefloor        # Play level trancefloor directly
python play.py --list-levels      # List all available levels
```

## Highscore Storage

The game supports **Vercel Postgres** for persistent highscore storage across all players:

- **Local play**: Can use either Vercel Postgres (recommended) or JSON file storage
- **Web deployment**: Uses Vercel Postgres for shared global highscores

**Quick setup:**
```bash
./setup.sh  # Automated setup script
```

For detailed instructions, see **[POSTGRES_SETUP.md](POSTGRES_SETUP.md)**

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
2. Install pygbag: `pip install pygbag`
3. Create a [Vercel account](https://vercel.com)
4. Login to Vercel: `vercel login`

### Automated Deployment

Simply run the deployment script:
```bash
./deploy.sh
```

This script will:
1. Build the web version with pygbag
2. Copy files to the `public/` directory
3. Commit and push changes to GitHub
4. Deploy to Vercel production

### Manual Deployment Steps

If you prefer manual deployment:

1. **Build web version:**
```bash
python -m pygbag --PYBUILD 3.12 --build .
```

2. **Copy to public directory:**
```bash
rm -rf public
mkdir -p public
cp -r build/web/* public/
```

3. **Deploy to Vercel:**
```bash
git add public
git commit -m "Update web build"
git push
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

For persistent highscore storage:

1. **Create Vercel Postgres database** in your Vercel dashboard
2. **Copy connection string** from database settings
3. **Add environment variable** to Vercel project:
   ```bash
   vercel env add POSTGRES_URL
   ```
4. **Run migration** (locally or via Vercel):
   ```bash
   python migrate_db.py
   ```

See **[POSTGRES_SETUP.md](POSTGRES_SETUP.md)** for complete instructions.

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
- sub level at the bar
- background
- the final enemy is yourself
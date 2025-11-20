# Web Build API Setup Guide

This guide explains how the HTTP API works for web builds (pygbag) and how to test it.

## Quick Start

The implementation automatically detects if running in a web environment and switches to using the HTTP API instead of direct database connections.

### Files Created

- `api/highscores.py` - Vercel serverless function for database operations
- `api/requirements.txt` - Dependencies for the serverless function
- `platformer/core/http_highscore_client.py` - Client for making HTTP requests from the game
- Updated `platformer/core/highscore_manager.py` - Auto-detects environment and routes appropriately
- Updated `vercel.json` - Configures serverless function deployment

## How It Works

### Environment Detection

The `HighscoreManager` automatically detects the runtime environment:

```python
import sys
IS_WEB_BUILD = sys.platform == "emscripten"
```

- **Desktop build**: Uses direct PostgreSQL connection
- **Web build (pygbag)**: Uses HTTP API client

### API Flow

```
Browser (WebAssembly Game)
    ↓ HTTP Request
/api/highscores (Vercel Serverless Function)
    ↓ SQL Query
PostgreSQL Database
    ↓ Results
Response to Browser
```

## Testing Locally

### Option 1: Test with Vercel Dev Server

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Run the development server:
```bash
vercel dev
```

3. The API will be available at `http://localhost:3000/api/highscores`

4. Test the endpoints:

**Get top scores:**
```bash
curl "http://localhost:3000/api/highscores?action=get_top_scores&level_name=test-level&limit=5"
```

**Check if score is a highscore:**
```bash
curl "http://localhost:3000/api/highscores?action=is_highscore&level_name=test-level&score=1000"
```

**Add a highscore:**
```bash
curl -X POST http://localhost:3000/api/highscores \
  -H "Content-Type: application/json" \
  -d '{
    "action": "add_highscore",
    "level_name": "test-level",
    "player_name": "TestPlayer",
    "score_breakdown": {
      "total_score": 1000,
      "time_score": 500,
      "trophy_score": 300,
      "damage_score": 150,
      "life_score": 50
    }
  }'
```

### Option 2: Test Pygbag Build Locally

1. Build with pygbag:
```bash
python -m pygbag --PYBUILD 3.12 .
```

2. In another terminal, run the Vercel dev server:
```bash
vercel dev
```

3. Open your browser and navigate to the pygbag build
4. The game should automatically use the HTTP API

## Environment Variables

Make sure `POSTGRES_URL` is set:

### Local (.env file):
```env
POSTGRES_URL=postgres://default:xxx@xxx.postgres.vercel-storage.com:5432/verceldb?sslmode=require
```

### Production (Vercel Dashboard):
1. Go to your Vercel project
2. Settings → Environment Variables
3. Add `POSTGRES_URL` (it may auto-populate if using Vercel Postgres)

## Deployment

### Deploy to Vercel

```bash
vercel --prod
```

This will:
1. Build the pygbag web build
2. Deploy the web files
3. Deploy the `/api/highscores` serverless function
4. Function will have access to environment variables

### Verify Deployment

After deployment, test the API:

```bash
# Replace your-domain.vercel.app with your actual domain
curl "https://your-domain.vercel.app/api/highscores?action=get_top_scores&level_name=test-level&limit=5"
```

## Code Examples

### Using HighscoreManager in Web Builds

The API is transparent - you use the same code for both desktop and web builds:

```python
from platformer.core.highscore_manager import HighscoreManager

# Initialize (auto-detects environment)
manager = HighscoreManager()

# For web builds, these methods return coroutines, so use await
if manager.use_http:
    # Web build - async
    scores = await manager.get_top_scores("level-1", limit=5)
    is_high = await manager.is_highscore("level-1", 1000)
    await manager.add_highscore("level-1", "Player", score_breakdown)
else:
    # Desktop build - synchronous
    scores = manager.get_top_scores("level-1", limit=5)
    is_high = manager.is_highscore("level-1", 1000)
    manager.add_highscore("level-1", "Player", score_breakdown)
```

### Or Use Helper Methods

If your game code is already async (which it should be for pygbag compatibility):

```python
# This works in both environments
async def save_highscore():
    manager = HighscoreManager()
    
    score_breakdown = manager.calculate_score(
        time_remaining=45.5,
        trophies_collected=3,
        damage_dealt=150,
        lives_remaining=2
    )
    
    # Check if it's a highscore
    result = manager.is_highscore("level-1", score_breakdown["total_score"])
    if manager.use_http:
        is_high = await result
    else:
        is_high = result
    
    if is_high:
        result = manager.add_highscore("level-1", "Player", score_breakdown)
        if manager.use_http:
            await result
```

## Troubleshooting

### API Returns 500 Error
- Check Vercel logs: `vercel logs`
- Verify `POSTGRES_URL` is set in environment variables
- Ensure database table exists (run migration)

### CORS Errors in Browser
- The API includes CORS headers automatically
- If still seeing errors, check browser console for details

### "Platform module not found" in Web Build
- This is expected - the `platform` module is provided by pygbag at runtime
- Don't worry if you see import errors during development

### Scores Not Saving
- Check browser developer console (F12) for errors
- Verify the API endpoint is accessible
- Test the API directly with curl commands

## API Endpoint Reference

See `api/README.md` for detailed API documentation.

## Performance Considerations

- API calls are asynchronous and won't block the game
- Failed API calls fall back gracefully
- Consider caching top scores locally to reduce API calls
- The API automatically handles connection pooling

## Security

- API validates all inputs
- Uses parameterized queries to prevent SQL injection
- CORS headers allow browser access while maintaining security
- Environment variables keep database credentials secure

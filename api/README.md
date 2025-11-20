# API Implementation for Pygbag/Web Builds

This directory contains Vercel serverless functions that provide PostgreSQL access for web builds of the game.

## Why This is Needed

When the game runs as a pygbag build (WebAssembly in browser), it cannot directly connect to PostgreSQL databases for security reasons. Instead, the game makes HTTP requests to these API endpoints, which run on the server and handle database operations.

## Files

- `highscores.py` - Main API endpoint for highscore operations
- `requirements.txt` - Python dependencies for the serverless functions

## API Endpoints

### POST /api/highscores
Add a new highscore entry.

**Request Body:**
```json
{
  "action": "add_highscore",
  "level_name": "level-1",
  "player_name": "Player1",
  "score_breakdown": {
    "total_score": 1000,
    "time_score": 500,
    "trophy_score": 300,
    "damage_score": 150,
    "life_score": 50
  }
}
```

**Response:**
```json
{
  "success": true,
  "id": 123
}
```

### GET /api/highscores?action=get_top_scores
Get top scores for a level.

**Query Parameters:**
- `action=get_top_scores`
- `level_name` - Name of the level
- `limit` - Number of scores to return (default: 5)

**Response:**
```json
{
  "scores": [
    {
      "player_name": "Player1",
      "score": 1000,
      "breakdown": {
        "total_score": 1000,
        "time_score": 500,
        "trophy_score": 300,
        "damage_score": 150,
        "life_score": 50
      },
      "timestamp": "2025-11-20T12:00:00"
    }
  ]
}
```

### GET /api/highscores?action=is_highscore
Check if a score qualifies as a highscore.

**Query Parameters:**
- `action=is_highscore`
- `level_name` - Name of the level
- `score` - Score to check

**Response:**
```json
{
  "is_highscore": true
}
```

## Environment Variables

The API requires the following environment variable to be set in your Vercel project:

- `POSTGRES_URL` - PostgreSQL connection string from Vercel Postgres

## Local Testing

To test the API locally with Vercel CLI:

```bash
vercel dev
```

Then access the API at `http://localhost:3000/api/highscores`

## Deployment

The API is automatically deployed when you push to your Vercel project. Make sure to:

1. Have Vercel Postgres set up in your project
2. Set the `POSTGRES_URL` environment variable
3. Deploy your project

The `vercel.json` configuration ensures these functions are deployed correctly.

# Vercel Postgres Setup Guide

This guide explains how to set up Vercel Postgres for highscore storage in both local development and production environments, including web builds (pygbag).

## Overview

The game now supports multiple storage backends for highscores depending on the environment:

### Desktop/Local Development (`python play.py`)
- **PostgreSQL** (via direct connection) - Primary option for best performance
- **JSON file** - Automatic fallback if PostgreSQL is not available

### Web Builds (pygbag/Vercel deployment)
- **PostgreSQL** (via HTTP API) - Browser-based games cannot connect directly to databases, so they use serverless API endpoints
- **JSON file** - Fallback if API is unavailable (embedded in the web build)

## Architecture

```
Desktop Build:
Game → DatabaseConnection → PostgreSQL

Web Build (pygbag):
Game (in browser) → HTTP API (/api/highscores) → PostgreSQL
```

## Prerequisites

- Vercel account
- Vercel CLI installed (`npm i -g vercel`)
- Python 3.x

## Setup Instructions

### 1. Create Vercel Postgres Database

1. Go to your Vercel dashboard
2. Navigate to your project (or create a new one)
3. Go to **Storage** tab
4. Click **Create Database**
5. Select **Postgres**
6. Choose a name for your database
7. Select a region (choose one close to your users)
8. Click **Create**

### 2. Get Your Connection String

1. After creating the database, go to the **Settings** tab of your database
2. Under **Connection String**, you'll find the `POSTGRES_URL`
3. Click to reveal and copy the full connection string
   - It should look like: `postgres://default:xxx@ep-xxx.us-east-1.postgres.vercel-storage.com:5432/verceldb?sslmode=require`

### 3. Configure Local Environment

1. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your connection string:
   ```env
   POSTGRES_URL=postgres://default:YOUR_PASSWORD@YOUR_HOST.postgres.vercel-storage.com:5432/verceldb?sslmode=require
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Initialize the Database

Run the migration script to create the highscores table:

```bash
python migrate_db.py
```

You should see:
```
🔄 Running database migrations...
✅ Highscores table created successfully
✅ Migration completed successfully!
```

### 5. Configure Vercel Deployment

For production deployment, add the environment variable to Vercel:

**Option A: Via Vercel Dashboard**
1. Go to your project settings on Vercel
2. Navigate to **Settings** → **Environment Variables**
3. Add a new variable:
   - Name: `POSTGRES_URL`
   - Value: Your connection string (it may auto-populate if you're using Vercel Postgres)
   - Environments: Production, Preview, Development

**Option B: Via Vercel CLI**
```bash
vercel env add POSTGRES_URL
```
Then paste your connection string when prompted.

### 6. Deploy

```bash
vercel --prod
```

## How It Works

### Desktop/Local Development (`python play.py`)

The `HighscoreManager` class automatically:
1. Detects it's running in a desktop environment
2. Checks if PostgreSQL is available (via environment variable)
3. If available and connection successful → uses direct PostgreSQL connection
4. If not available → falls back to JSON file storage

**Local Development:**
- Set `POSTGRES_URL` in `.env` → uses Vercel Postgres directly
- No `.env` file → uses local JSON file (`platformer/assets/highscores.json`)

### Web Builds (pygbag/Vercel)

For web builds, direct database connections are not possible due to browser security restrictions. Instead:

1. Detects it's running in emscripten/WebAssembly environment
2. Uses HTTP API client to communicate with serverless functions
3. Serverless functions (`/api/highscores`) handle database operations
4. Falls back to embedded JSON if API is unavailable

**Production (Vercel):**
- Web build → uses `/api/highscores` endpoint → PostgreSQL
- API requires `POSTGRES_URL` environment variable set in Vercel project settings

## Database Schema

```sql
CREATE TABLE highscores (
    id SERIAL PRIMARY KEY,
    level_name VARCHAR(255) NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    total_score INTEGER NOT NULL,
    time_score INTEGER NOT NULL,
    trophy_score INTEGER NOT NULL,
    damage_score INTEGER NOT NULL,
    life_score INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_level_score ON highscores(level_name, total_score DESC);
```

## Testing

### Test Local Connection

```python
from platformer.core.database import is_postgres_available, create_highscores_table

# Check if connection works
if is_postgres_available():
    print("✅ PostgreSQL connection successful!")
else:
    print("❌ PostgreSQL not available")
```

### Test Highscore Manager

```python
from platformer.core.highscore_manager import HighscoreManager

manager = HighscoreManager()

# Add a test score
score_breakdown = manager.calculate_score(
    time_remaining=45.5,
    trophies_collected=3,
    damage_dealt=150,
    lives_remaining=2
)

manager.add_highscore("test-level", "TestPlayer", score_breakdown)

# Retrieve scores
top_scores = manager.get_top_scores("test-level")
print(top_scores)
```

## Troubleshooting

### "POSTGRES_URL environment variable not set"
- Make sure you've created a `.env` file with the correct connection string
- Verify the `.env` file is in the project root directory
- Check that `python-dotenv` is installed

### "Failed to create connection pool"
- Verify your connection string is correct
- Check your internet connection
- Ensure your IP is not blocked (Vercel Postgres allows all IPs by default)
- Check if the database exists in your Vercel dashboard

### Falls back to JSON file unexpectedly
- Check console output for error messages
- Verify `POSTGRES_URL` is set correctly
- Run `python migrate_db.py` to ensure tables exist
- Test connection with the test script above

### Import errors for psycopg2 or dotenv
- Run `pip install -r requirements.txt`
- If on macOS and getting psycopg2 build errors, try: `pip install psycopg2-binary`

## Benefits of Vercel Postgres

1. **Unified Storage**: Same database for local development and production
2. **Real-time Sync**: All players share the same highscore table
3. **Scalability**: Handles multiple concurrent connections
4. **Reliability**: Automatic backups and high availability
5. **Performance**: Optimized queries with indexes
6. **Free Tier**: Generous free tier for hobby projects

## Migrating Existing JSON Highscores

If you have existing highscores in JSON format that you want to migrate:

```python
import json
from platformer.core.highscore_manager import HighscoreManager

# Load old JSON data
with open('platformer/assets/highscores.json', 'r') as f:
    old_scores = json.load(f)

# Create manager with Postgres enabled
manager = HighscoreManager(use_postgres=True)

# Migrate each score
for level_name, scores in old_scores.items():
    for entry in scores:
        manager.add_highscore(
            level_name,
            entry['player_name'],
            entry['breakdown']
        )

print("Migration complete!")
```

## Security Notes

- **Never commit `.env`** to version control (already in `.gitignore`)
- Connection strings contain sensitive credentials
- Vercel automatically encrypts environment variables
- Use environment variables for all sensitive data

## Further Reading

- [Vercel Postgres Documentation](https://vercel.com/docs/storage/vercel-postgres)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

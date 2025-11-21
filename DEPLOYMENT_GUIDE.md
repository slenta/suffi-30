# Vercel API Deployment Guide

Follow these steps to deploy your highscore API to Vercel.

## Prerequisites

✅ Vercel CLI installed (you have this)
✅ Vercel account
✅ Project files ready (you have this)

## Step 1: Create Vercel Postgres Database

1. Go to https://vercel.com/dashboard
2. Click on your project (or create a new one if needed)
3. Click on the **Storage** tab
4. Click **Create Database**
5. Select **Postgres**
6. Name it something like `suffi-highscores`
7. Select a region close to you
8. Click **Create**

## Step 2: Initialize the Database

The database needs a table to store highscores. Run this SQL in your Vercel Postgres dashboard:

1. In your database, go to the **Query** tab
2. Paste this SQL:

```sql
CREATE TABLE IF NOT EXISTS highscores (
    id SERIAL PRIMARY KEY,
    level_name VARCHAR(100) NOT NULL,
    player_name VARCHAR(50) NOT NULL,
    total_score INTEGER NOT NULL,
    time_score INTEGER NOT NULL,
    trophy_score INTEGER NOT NULL,
    damage_score INTEGER NOT NULL,
    life_score INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_highscores_level_score 
ON highscores(level_name, total_score DESC);
```

3. Click **Run Query**

## Step 3: Deploy to Vercel

Now deploy your project:

```bash
cd /Users/david/code/suffi-30
vercel --prod
```

The deployment will:
- Build your static site from `build/web`
- Deploy the API functions from `api/`
- Automatically connect to your Postgres database

## Step 4: Verify Deployment

After deployment completes, Vercel will show you a URL like:
```
https://your-project-name.vercel.app
```

Test the API:

```bash
# Replace with your actual Vercel URL
curl "https://your-project-name.vercel.app/api/highscores?action=get_top_scores&level_name=test-level&limit=5"
```

You should get a JSON response (might be empty if no scores yet):
```json
{"scores": []}
```

## Step 5: Update Your Local Configuration (Optional)

If you want to test locally with the deployed API:

1. Edit `platformer/config/api_config.py`
2. Set your Vercel URL:
   ```python
   API_BASE_URL = "https://your-project-name.vercel.app/api"
   ```

3. Test locally:
   ```bash
   python test_api.py
   ```

## Step 6: Test the Full Flow

1. **Build your game for web:**
   ```bash
   pygbag --build .
   ```

2. **Serve locally:**
   ```bash
   python -m http.server 8000 --directory build/web
   ```

3. **Open in browser:**
   ```
   http://localhost:8000
   ```

4. **Play the game and complete a level**

5. **Check your Vercel Postgres dashboard:**
   - Go to your database
   - Click **Data** tab
   - Select the `highscores` table
   - You should see your score!

## Troubleshooting

### API returns 500 error
- Check Vercel logs: `vercel logs`
- Verify `POSTGRES_URL` environment variable is set
- Check the SQL table was created correctly

### CORS errors in browser
- The API already includes CORS headers
- Make sure you're accessing via the deployed URL or localhost

### Scores not saving
- Check browser console for error messages
- Verify the API endpoint is accessible
- Check Vercel function logs

## Environment Variables

Vercel automatically sets these when you add a Postgres database:
- `POSTGRES_URL` - Full connection string
- `POSTGRES_PRISMA_URL` - Prisma-compatible URL
- `POSTGRES_URL_NON_POOLING` - Direct connection URL

Your API code uses `POSTGRES_URL`.

## Quick Commands Reference

```bash
# Deploy to production
vercel --prod

# Deploy to preview
vercel

# Check logs
vercel logs

# List deployments
vercel ls

# Run locally with Vercel dev server
vercel dev
```

## What Happens After Deployment

1. **Deployed site** (e.g., https://your-app.vercel.app):
   - Game auto-detects it's on the deployed domain
   - Uses `/api/highscores` automatically
   - Stores data in Postgres ✅

2. **Local pygbag testing** (http://localhost:8000):
   - Falls back to localStorage
   - Works offline for testing ✅

3. **Desktop Python** (python play.py):
   - Uses direct Postgres if configured
   - Falls back to JSON file ✅

All three scenarios work seamlessly!

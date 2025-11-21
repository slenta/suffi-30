# Debugging Highscore Issues - Browser Console Checklist

## Step 1: Open Browser Console
1. Go to https://suffi-30.vercel.app
2. Press F12 (or Cmd+Option+I on Mac)
3. Click on the "Console" tab
4. Clear any old messages

## Step 2: Check Initial Load Messages
When the game loads, you should see:
```
🌐 Running in web environment - using HTTP API for highscores
🌐 Detected origin: https://suffi-30.vercel.app
✅ Using HTTP API for highscore storage: /api
```

**If you DON'T see these:**
- The build might be old
- Run: `./rebuild_and_deploy.sh`

**If you see "Using localStorage" instead:**
- The API detection failed
- Check the error messages in console

## Step 3: Play the Game
1. Complete a level
2. Enter your name when prompted
3. Watch the console for these messages:

```
📤 Fetching POST /api/highscores
📤 Request body: {"action":"add_highscore"...
📥 Response status: 200
📥 Response text: {"success":true...
💾 Highscore saved for [name]: [score]
```

## Step 4: Check Top Scores Display
When the game shows top scores, you should see:
```
📥 Fetching GET /api/highscores?action=get_top_scores...
📥 Response status: 200
📥 Response text: {"scores":[...
✅ Retrieved X scores from API
```

## Step 5: If Nothing Appears

### A. Hard Refresh the Page
- Windows/Linux: Ctrl+Shift+R
- Mac: Cmd+Shift+R
This clears browser cache

### B. Check Network Tab
1. Open F12 → "Network" tab
2. Filter by "Fetch/XHR"
3. Play the game
4. Look for requests to `/api/highscores`
5. Click on them to see:
   - Request headers
   - Request payload
   - Response

### C. Verify Latest Build is Deployed
Run these commands:
```bash
# Check current deployment
vercel ls

# The first one should be recent (within minutes of your last deploy)
```

## Step 6: Manual API Test from Console

Open browser console on https://suffi-30.vercel.app and paste:

```javascript
// Test fetch
fetch('/api/highscores?action=get_top_scores&level_name=test-level&limit=5')
  .then(r => r.json())
  .then(data => console.log('API Response:', data))
  .catch(err => console.error('API Error:', err));
```

You should see:
```
API Response: {scores: Array(2)}
```

## Step 7: Check Vercel Function Logs

Go to:
1. https://vercel.com/dashboard
2. Click on your "suffi-30" project
3. Click "Functions" tab
4. Click on "api/highscores.py"
5. See the invocation logs

## Common Issues & Solutions

### Issue: "platform.window not available"
**Solution**: Rebuild with latest pygbag
```bash
python -m pygbag --build --template custom.tmpl .
vercel --prod
```

### Issue: CORS errors in console
**Solution**: The API already has CORS headers, but check:
- Is the request going to the same domain?
- Use relative URL `/api` not absolute URL

### Issue: "localStorage" being used instead of API
**Solution**: Check initialization:
- Look for "✅ Using HTTP API" message
- If not present, API detection failed
- Check browser console for errors during load

### Issue: No console messages at all
**Solution**: 
1. Make sure console is set to show "All levels" (not just Errors)
2. Try different browser (Chrome/Firefox)
3. Disable browser extensions that might block console.log

## Quick Test Commands

### Test API directly (from terminal):
```bash
# Add a score
curl -X POST https://suffi-30.vercel.app/api/highscores \
  -H "Content-Type: application/json" \
  -d '{"action":"add_highscore","level_name":"test","player_name":"Test","score_breakdown":{"total_score":999,"time_score":500,"trophy_score":300,"damage_score":150,"life_score":49}}'

# Get scores
curl "https://suffi-30.vercel.app/api/highscores?action=get_top_scores&level_name=test&limit=5"
```

### Test from browser console (paste this):
```javascript
// Add highscore
fetch('/api/highscores', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    action: 'add_highscore',
    level_name: 'browser-test',
    player_name: 'BrowserTest',
    score_breakdown: {
      total_score: 8888,
      time_score: 4000,
      trophy_score: 2000,
      damage_score: 1000,
      life_score: 1888
    }
  })
})
.then(r => r.json())
.then(d => console.log('Added:', d));
```

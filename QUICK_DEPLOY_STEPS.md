# ⚡ Quick Deploy to Railway (5 Minutes)

## TL;DR - Fast Track

### Step 1: Prepare Code (Already Done ✅)
- ✅ `.gitignore` created
- ✅ `.env.example` created
- ✅ `Procfile` created
- ✅ `requirements.txt` updated
- ✅ `fastapi_chatbot.py` updated for env vars

### Step 2: Push to GitHub
```bash
cd c:\Users\aldri\OneDrive\Desktop\chunk

# Initialize git if needed
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Railway deployment"

# Create repo on GitHub.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/vector-db-chatbot.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Railway (2 clicks)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `vector-db-chatbot` repo
5. Click "Deploy"

### Step 4: Add Environment Variables
In Railway dashboard:
1. Click your project
2. Go to "Variables" tab
3. Add:
   ```
   COHERE_API_KEY=your_key_here
   DB_PATH=./vector_db
   COLLECTION_NAME=definitions
   ALLOWED_ORIGINS=*
   ```
4. Save

### Step 5: Get Your URL
1. Go to "Settings" tab
2. Copy "Public URL"
3. Use in Android app: `https://your-railway-url`

---

## Testing Your Deployment

### Test Health
```bash
curl https://your-railway-url/health
```

### Test Chat
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is PRMSU?"}'
```

### View Logs
- Railway Dashboard → Logs tab

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Chatbot not initialized" | Add `COHERE_API_KEY` to Variables |
| "ModuleNotFoundError" | Check `requirements.txt` has all packages |
| Slow first request | Normal (5-10 sec) on free tier |
| Vector DB not found | Check `DB_PATH=./vector_db` in Variables |

---

## Your Deployment URL
Once deployed, your API will be at:
```
https://your-railway-url/docs
```

Use this in your Android app!

---

## Need Help?
- Full guide: See `RAILWAY_DEPLOYMENT_GUIDE.md`
- Railway docs: https://docs.railway.app
- FastAPI docs: https://fastapi.tiangolo.com



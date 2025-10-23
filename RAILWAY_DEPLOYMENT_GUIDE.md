# 🚀 Railway Deployment Guide

Complete step-by-step guide to deploy your FastAPI Vector Database Chatbot to Railway.

## Prerequisites

- GitHub account (free)
- Railway account (free)
- Your Cohere API key
- Git installed on your computer

---

## Step 1: Prepare Your Local Repository

### 1.1 Initialize Git (if not already done)
```bash
cd c:\Users\aldri\OneDrive\Desktop\chunk
git init
git add .
git commit -m "Initial commit: FastAPI chatbot with vector database"
```

### 1.2 Create `.env` file locally (for testing)
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your Cohere API key
# COHERE_API_KEY=your_actual_api_key_here
```

### 1.3 Test locally
```bash
pip install -r requirements.txt
python fastapi_chatbot.py
```
Visit: http://localhost:8000/docs

---

## Step 2: Push to GitHub

### 2.1 Create a new GitHub repository
1. Go to https://github.com/new
2. Name it: `vector-db-chatbot`
3. Choose "Private" (to keep your API key safe)
4. Click "Create repository"

### 2.2 Push your code
```bash
git remote add origin https://github.com/YOUR_USERNAME/vector-db-chatbot.git
git branch -M main
git push -u origin main
```

---

## Step 3: Set Up Railway Account

### 3.1 Create Railway Account
1. Go to https://railway.app
2. Click "Start Free"
3. Sign up with GitHub (recommended)
4. Authorize Railway to access your GitHub

### 3.2 Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Select your `vector-db-chatbot` repository
4. Click "Deploy"

---

## Step 4: Configure Environment Variables

### 4.1 Add Environment Variables in Railway
1. In Railway dashboard, go to your project
2. Click on the "fastapi_chatbot" service
3. Go to "Variables" tab
4. Add the following variables:

```
COHERE_API_KEY=your_actual_cohere_api_key_here
DB_PATH=./vector_db
COLLECTION_NAME=definitions
ALLOWED_ORIGINS=*
PORT=8000
HOST=0.0.0.0
```

**Important:** 
- Replace `your_actual_cohere_api_key_here` with your real Cohere API key
- Keep `ALLOWED_ORIGINS=*` for now (update later for production)

### 4.2 Verify Variables
- Click "Save"
- Railway will automatically redeploy with new variables

---

## Step 5: Monitor Deployment

### 5.1 Check Deployment Status
1. Go to "Deployments" tab
2. Watch the build progress
3. Look for green checkmark when complete

### 5.2 View Logs
1. Click "Logs" tab
2. You should see:
   ```
   ✅ Chatbot initialized successfully
   📊 Database contains XXX definitions
   ```

### 5.3 Get Your Public URL
1. Go to "Settings" tab
2. Look for "Public URL" or "Domain"
3. Copy the URL (e.g., `https://vector-db-chatbot-production.up.railway.app`)

---

## Step 6: Test Your Deployed API

### 6.1 Test Health Endpoint
```bash
curl https://your-railway-url/health
```

Expected response:
```json
{
  "status": "healthy",
  "database_count": 1234,
  "api_connected": true
}
```

### 6.2 Test Chat Endpoint
```bash
curl -X POST https://your-railway-url/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is PRMSU?"}'
```

### 6.3 Test in Android Studio
Update your Android app to use:
```
BASE_URL = "https://your-railway-url"
```

---

## Step 7: Update CORS for Production

### 7.1 Get Your Android App Domain
- If using localhost: `http://localhost:8080`
- If deployed: `https://yourandroidapp.com`

### 7.2 Update ALLOWED_ORIGINS
1. Go to Railway dashboard
2. Click "Variables"
3. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS=http://localhost:8080,https://yourandroidapp.com
   ```
4. Save (Railway will redeploy)

---

## Troubleshooting

### Issue: "Chatbot not initialized"
**Solution:** Check that `COHERE_API_KEY` is set in Variables

### Issue: "ModuleNotFoundError"
**Solution:** Ensure all packages in `requirements.txt` are listed

### Issue: "Port already in use"
**Solution:** Railway automatically assigns PORT via environment variable (already handled)

### Issue: Vector DB not persisting
**Solution:** Railway volumes persist by default. Check "Volumes" tab in settings.

### Issue: Slow first request
**Solution:** Normal for Railway free tier. First request takes 5-10 seconds.

---

## Monitoring & Maintenance

### View Real-time Logs
```bash
# In Railway dashboard, click "Logs" tab
# Logs update in real-time
```

### Check Resource Usage
1. Go to "Metrics" tab
2. Monitor CPU, Memory, Network

### Redeploy After Code Changes
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
# Railway automatically redeploys
```

---

## Free Tier Limits

- **500 hours/month** = ~16 hours/day continuous
- **5 GB storage** (your vector_db is 35 MB ✅)
- **Unlimited requests** (within fair use)
- **Auto-scaling** included

---

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Test all endpoints
3. ✅ Update Android app with Railway URL
4. ✅ Monitor logs for errors
5. Consider upgrading to paid tier if you need 24/7 uptime

---

## Support

- Railway Docs: https://docs.railway.app
- FastAPI Docs: https://fastapi.tiangolo.com
- Cohere API Docs: https://docs.cohere.com



# 🔧 Exact Commands to Deploy

Copy and paste these commands in order. Replace placeholders with your actual values.

---

## Step 1: Initialize Git & Push to GitHub

### 1.1 Open PowerShell and navigate to your project
```powershell
cd c:\Users\aldri\OneDrive\Desktop\chunk
```

### 1.2 Initialize Git repository
```powershell
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 1.3 Add all files
```powershell
git add .
```

### 1.4 Create first commit
```powershell
git commit -m "Initial commit: FastAPI chatbot ready for Railway deployment"
```

### 1.5 Create repository on GitHub
1. Go to https://github.com/new
2. Name: `vector-db-chatbot`
3. Description: "FastAPI Vector Database Chatbot for Android"
4. Choose "Private"
5. Click "Create repository"

### 1.6 Connect local repo to GitHub
Replace `YOUR_USERNAME` with your GitHub username:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/vector-db-chatbot.git
git branch -M main
git push -u origin main
```

---

## Step 2: Create Railway Account

1. Go to https://railway.app
2. Click "Start Free"
3. Click "Continue with GitHub"
4. Authorize Railway
5. You're in! ✅

---

## Step 3: Deploy on Railway

1. In Railway dashboard, click "New Project"
2. Click "Deploy from GitHub repo"
3. Select your `vector-db-chatbot` repository
4. Click "Deploy"
5. Wait 2-5 minutes for build to complete

---

## Step 4: Add Environment Variables

In Railway dashboard:

1. Click on your project
2. Click on the "fastapi_chatbot" service
3. Go to "Variables" tab
4. Click "Add Variable" and add these one by one:

```
COHERE_API_KEY=m7uIZhmn9itLRlZmEvHVwIJ6nvJ0FU2zZ5vd40e9
DB_PATH=./vector_db
COLLECTION_NAME=definitions
ALLOWED_ORIGINS=*
PORT=8000
HOST=0.0.0.0
```

5. Click "Save"
6. Railway will automatically redeploy

---

## Step 5: Get Your Public URL

1. In Railway dashboard, go to "Settings" tab
2. Look for "Public URL" or "Domain"
3. Copy the URL (looks like: `https://vector-db-chatbot-production.up.railway.app`)
4. Save this URL - you'll need it for your Android app

---

## Step 6: Test Your Deployment

### Test 1: Health Check
```powershell
$url = "https://your-railway-url/health"
Invoke-WebRequest -Uri $url | ConvertTo-Json
```

Expected response:
```json
{
  "status": "healthy",
  "database_count": 1234,
  "api_connected": true
}
```

### Test 2: Chat Endpoint
```powershell
$url = "https://your-railway-url/chat"
$body = @{
    question = "What is PRMSU?"
    max_results = 5
} | ConvertTo-Json

Invoke-WebRequest -Uri $url `
  -Method POST `
  -ContentType "application/json" `
  -Body $body | ConvertTo-Json
```

### Test 3: View API Documentation
Open in browser:
```
https://your-railway-url/docs
```

---

## Step 7: Update Android App

In your Android Studio project, update the API base URL:

```kotlin
// Before
const val BASE_URL = "http://localhost:8000/"

// After
const val BASE_URL = "https://your-railway-url/"
```

Then rebuild and test your Android app.

---

## Step 8: Update CORS for Production (Optional)

If you want to restrict access to only your Android app:

1. In Railway dashboard, go to "Variables"
2. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS=https://yourandroidapp.com
   ```
3. Click "Save"

---

## Troubleshooting Commands

### Check if Git is installed
```powershell
git --version
```

### View Git status
```powershell
git status
```

### View recent commits
```powershell
git log --oneline -5
```

### Test API locally before deploying
```powershell
pip install -r requirements.txt
python fastapi_chatbot.py
```

Then visit: http://localhost:8000/docs

---

## Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Your GitHub Repos: https://github.com/YOUR_USERNAME?tab=repositories
- FastAPI Docs: https://fastapi.tiangolo.com
- Cohere API: https://docs.cohere.com

---

## Quick Reference

| What | Where |
|------|-------|
| Your API | `https://your-railway-url` |
| API Docs | `https://your-railway-url/docs` |
| Health Check | `https://your-railway-url/health` |
| Chat Endpoint | `https://your-railway-url/chat` |
| Search Endpoint | `https://your-railway-url/search` |

---

## Next Steps After Deployment

1. ✅ Test all endpoints
2. ✅ Update Android app with new URL
3. ✅ Monitor logs for errors
4. ✅ Test from Android device
5. ✅ Share API URL with team



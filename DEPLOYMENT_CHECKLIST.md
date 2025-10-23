# ✅ Railway Deployment Checklist

## Pre-Deployment (Code Preparation) ✅ DONE

- [x] Create `.gitignore` - Excludes sensitive files
- [x] Create `.env.example` - Template for environment variables
- [x] Create `Procfile` - Tells Railway how to run your app
- [x] Create `runtime.txt` - Specifies Python 3.11.7
- [x] Update `fastapi_chatbot.py` - Uses environment variables
- [x] Update `requirements.txt` - Added python-dotenv

## Deployment Steps (Do These Now)

### Phase 1: GitHub Setup
- [ ] Create GitHub account (if needed): https://github.com/signup
- [ ] Create new repository named `vector-db-chatbot`
- [ ] Push your code to GitHub:
  ```bash
  git init
  git add .
  git commit -m "Ready for Railway deployment"
  git remote add origin https://github.com/YOUR_USERNAME/vector-db-chatbot.git
  git branch -M main
  git push -u origin main
  ```

### Phase 2: Railway Setup
- [ ] Create Railway account: https://railway.app
- [ ] Sign up with GitHub (recommended)
- [ ] Create new project
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose your `vector-db-chatbot` repository
- [ ] Click "Deploy"

### Phase 3: Configuration
- [ ] Wait for build to complete (2-5 minutes)
- [ ] Go to "Variables" tab
- [ ] Add environment variables:
  - [ ] `COHERE_API_KEY` = your actual API key
  - [ ] `DB_PATH` = ./vector_db
  - [ ] `COLLECTION_NAME` = definitions
  - [ ] `ALLOWED_ORIGINS` = *
  - [ ] `PORT` = 8000
  - [ ] `HOST` = 0.0.0.0
- [ ] Click "Save" (auto-redeploy)

### Phase 4: Verification
- [ ] Check "Logs" tab for success messages
- [ ] Look for: "✅ Chatbot initialized successfully"
- [ ] Look for: "📊 Database contains XXX definitions"
- [ ] Copy your public URL from "Settings" tab

### Phase 5: Testing
- [ ] Test health endpoint:
  ```bash
  curl https://your-railway-url/health
  ```
- [ ] Test chat endpoint:
  ```bash
  curl -X POST https://your-railway-url/chat \
    -H "Content-Type: application/json" \
    -d '{"question": "What is PRMSU?"}'
  ```
- [ ] Visit API docs: `https://your-railway-url/docs`

### Phase 6: Android Integration
- [ ] Update Android app BASE_URL to your Railway URL
- [ ] Test API calls from Android app
- [ ] Verify CORS is working (no CORS errors)

## Post-Deployment

### Security
- [ ] Update `ALLOWED_ORIGINS` with your Android app domain
- [ ] Never commit `.env` file (use `.env.example` instead)
- [ ] Keep Cohere API key secret

### Monitoring
- [ ] Check Railway logs regularly
- [ ] Monitor resource usage (CPU, Memory)
- [ ] Set up alerts for errors

### Maintenance
- [ ] Test API weekly
- [ ] Update code as needed (auto-deploys on git push)
- [ ] Monitor free tier usage (500 hours/month)

## Troubleshooting

### Build Failed
- Check "Logs" tab for error messages
- Ensure all dependencies in `requirements.txt`
- Verify Python version in `runtime.txt`

### API Not Responding
- Check if service is running (green status)
- Verify environment variables are set
- Check logs for initialization errors

### Vector DB Issues
- Ensure `DB_PATH=./vector_db` is set
- Check that vector_db folder is in repository
- Verify database has definitions

### CORS Errors
- Update `ALLOWED_ORIGINS` in Variables
- Include your Android app's domain
- Restart service after updating

## Resources

- **Full Guide:** `RAILWAY_DEPLOYMENT_GUIDE.md`
- **Quick Steps:** `QUICK_DEPLOY_STEPS.md`
- **Railway Docs:** https://docs.railway.app
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Cohere API:** https://docs.cohere.com

## Timeline

- **Code Prep:** ✅ 5 minutes (DONE)
- **GitHub Setup:** 5 minutes
- **Railway Setup:** 2 minutes
- **Configuration:** 3 minutes
- **Build & Deploy:** 5 minutes
- **Testing:** 5 minutes

**Total Time: ~25 minutes**

---

## Your Deployment URL

Once complete, your API will be available at:
```
https://your-railway-url
```

Share this with your Android app!



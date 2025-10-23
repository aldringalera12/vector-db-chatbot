# 🚀 Quick Start: Deploy on Render.com + AWS S3

## 📋 What You Need

1. **AWS Account** (free)
2. **Render Account** (free)
3. **GitHub Account** (already have it)

---

## ⏱️ 30-Minute Setup

### Phase 1: AWS Setup (10 min)

**Step 1: Create AWS Account**
- Go to https://aws.amazon.com/
- Sign up with email

**Step 2: Create S3 Bucket**
- Go to https://s3.console.aws.amazon.com/
- Click "Create bucket"
- Name: `your-name-vector-db`
- Region: `us-east-1`

**Step 3: Get AWS Credentials**
- Go to https://console.aws.amazon.com/
- Click account name → Security credentials
- Click "Access keys" → "Create access key"
- **SAVE:**
  - Access Key ID
  - Secret Access Key

---

### Phase 2: Code Update (Already Done!)

✅ I've already updated your code:
- Added `s3_utils.py` - S3 storage manager
- Updated `requirements.txt` - Added boto3
- Updated `fastapi_chatbot.py` - S3 integration
- All changes pushed to GitHub

---

### Phase 3: Render Deployment (10 min)

**Step 1: Create Render Account**
- Go to https://render.com
- Click "Get started"
- Sign up with GitHub

**Step 2: Create Web Service**
- Go to https://dashboard.render.com
- Click "New +" → "Web Service"
- Select your repo: `vector-db-chatbot`
- Click "Connect"

**Step 3: Configure Service**
- **Name:** `vector-db-chatbot`
- **Environment:** `Python 3`
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn fastapi_chatbot:app --host 0.0.0.0 --port $PORT`

**Step 4: Add Environment Variables**
```
COHERE_API_KEY=m7uIZhmn9itLRlZmEvHVwIJ6nvJ0FU2zZ5vd40e9
DB_PATH=./vector_db
COLLECTION_NAME=definitions
ALLOWED_ORIGINS=*
AWS_ACCESS_KEY_ID=<your_access_key_id>
AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
AWS_S3_BUCKET=<your-bucket-name>
AWS_REGION=us-east-1
```

**Step 5: Deploy**
- Click "Create Web Service"
- Wait 5-10 minutes

---

### Phase 4: Verify (5 min)

**Test 1: Health Check**
```powershell
curl https://your-render-url/health
```

**Test 2: Chat**
```powershell
curl -X POST https://your-render-url/chat `
  -H "Content-Type: application/json" `
  -d '{"question": "What is PRMSU?"}'
```

**Test 3: Check S3**
- Go to https://s3.console.aws.amazon.com/
- Should see `vector_db.zip` in your bucket

---

## ✅ Success!

Your app is now:
- ✅ Deployed on Render (free tier)
- ✅ Database backed up to AWS S3 (free tier)
- ✅ Persistent across deployments
- ✅ Ready for Android app

---

## 📚 Detailed Guides

- **DEPLOY_RENDER_STEP_BY_STEP.md** - Full step-by-step guide
- **RENDER_AWS_SETUP.md** - Detailed AWS setup
- **DEPLOY_COMMANDS.md** - Copy/paste commands

---

## 🎯 Your API URL

After deployment, you'll get a URL like:
```
https://vector-db-chatbot-xxxx.onrender.com
```

**Update your Android app with this URL!**

---

## 💡 How It Works

1. **App starts** → Downloads database from S3
2. **User asks question** → App searches database
3. **App shuts down** → Uploads database to S3
4. **Next deployment** → Downloads updated database

This way your database persists across deployments! 🎉

---

## 📞 Need Help?

Check these files:
- **DEPLOY_RENDER_STEP_BY_STEP.md** - Detailed steps
- **RENDER_AWS_SETUP.md** - AWS setup details
- **CRASH_FIX.md** - If app crashes



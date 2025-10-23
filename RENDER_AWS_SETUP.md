# 🚀 Deploy on Render.com + AWS S3 (FREE)

## 📋 Overview

1. **Render.com** - Hosts your FastAPI app (free)
2. **AWS S3** - Stores your vector_db (free)
3. **Your App** - Loads/saves database from S3

---

## ⏱️ Total Time: ~30 minutes

---

## PART 1: AWS S3 Setup (10 minutes)

### Step 1: Create AWS Account
1. Go to https://aws.amazon.com/
2. Click "Create AWS Account"
3. Fill in email, password, account name
4. Add payment method (won't charge for free tier)
5. Verify email

### Step 2: Create S3 Bucket
1. Go to https://s3.console.aws.amazon.com/
2. Click "Create bucket"
3. **Bucket name:** `your-name-vector-db` (must be unique)
4. **Region:** `us-east-1` (closest to you)
5. Click "Create bucket"

### Step 3: Get AWS Credentials
1. Go to https://console.aws.amazon.com/
2. Click your account name (top right)
3. Click "Security credentials"
4. Click "Access keys"
5. Click "Create access key"
6. Choose "Application running outside AWS"
7. Click "Create access key"
8. **SAVE THESE:**
   - Access Key ID
   - Secret Access Key

**⚠️ IMPORTANT:** Save these securely! You'll need them for Render.

---

## PART 2: Update Your Code (10 minutes)

I'll modify your app to use S3 for storage.

### Files to Update:
1. `requirements.txt` - Add boto3 (AWS SDK)
2. `fastapi_chatbot.py` - Add S3 upload/download
3. `definition_chunker.py` - Use S3 for persistence

---

## PART 3: Deploy on Render (10 minutes)

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get started"
3. Sign up with GitHub
4. Authorize Render

### Step 2: Create Web Service
1. Go to https://dashboard.render.com
2. Click "New +"
3. Click "Web Service"
4. Connect your GitHub repo
5. Fill in:
   - **Name:** `vector-db-chatbot`
   - **Environment:** `Python 3`
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn fastapi_chatbot:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables
1. Scroll down to "Environment"
2. Add these variables:
   ```
   COHERE_API_KEY=m7uIZhmn9itLRlZmEvHVwIJ6nvJ0FU2zZ5vd40e9
   DB_PATH=./vector_db
   COLLECTION_NAME=definitions
   ALLOWED_ORIGINS=*
   
   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   AWS_S3_BUCKET=your-bucket-name
   AWS_REGION=us-east-1
   ```

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for build
3. Get your URL from dashboard

---

## ✅ Verification

### Test 1: Health Check
```powershell
curl https://your-render-url/health
```

### Test 2: Chat
```powershell
curl -X POST https://your-render-url/chat `
  -H "Content-Type: application/json" `
  -d '{"question": "What is PRMSU?"}'
```

### Test 3: Check S3
1. Go to https://s3.console.aws.amazon.com/
2. Click your bucket
3. Should see `vector_db.zip` file

---

## 📚 Next Steps

1. Read this guide
2. Create AWS account
3. Create S3 bucket
4. Get AWS credentials
5. I'll update your code
6. Deploy on Render
7. Test endpoints
8. Done! 🎉



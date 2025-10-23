# 🚀 Deploy on Render.com + AWS S3 (Step-by-Step)

## ⏱️ Total Time: ~30 minutes

---

## STEP 1: Create AWS Account & S3 Bucket (10 minutes)

### 1.1 Create AWS Account
1. Go to https://aws.amazon.com/
2. Click "Create AWS Account"
3. Enter email, password, account name
4. Add payment method (won't charge for free tier)
5. Verify email

### 1.2 Create S3 Bucket
1. Go to https://s3.console.aws.amazon.com/
2. Click "Create bucket"
3. **Bucket name:** `your-name-vector-db` (must be unique, use your name)
4. **Region:** `us-east-1`
5. Click "Create bucket"

### 1.3 Get AWS Credentials
1. Go to https://console.aws.amazon.com/
2. Click your account name (top right)
3. Click "Security credentials"
4. Click "Access keys"
5. Click "Create access key"
6. Choose "Application running outside AWS"
7. Click "Create access key"

**⚠️ SAVE THESE (you'll need them):**
```
Access Key ID: ___________________
Secret Access Key: ___________________
```

---

## STEP 2: Commit Code Changes (5 minutes)

### 2.1 Commit to GitHub
```powershell
cd c:\Users\aldri\OneDrive\Desktop\chunk
git add .
git commit -m "Add S3 support for database persistence"
git push origin main
```

### 2.2 Verify Push
Go to https://github.com/aldringalera12/vector-db-chatbot
Should see new files:
- `s3_utils.py`
- Updated `requirements.txt`
- Updated `fastapi_chatbot.py`

---

## STEP 3: Create Render Account (5 minutes)

### 3.1 Sign Up
1. Go to https://render.com
2. Click "Get started"
3. Click "Sign up with GitHub"
4. Authorize Render

### 3.2 Create Web Service
1. Go to https://dashboard.render.com
2. Click "New +"
3. Click "Web Service"
4. Select your GitHub repo: `vector-db-chatbot`
5. Click "Connect"

---

## STEP 4: Configure Render Service (5 minutes)

### 4.1 Fill in Service Details
- **Name:** `vector-db-chatbot`
- **Environment:** `Python 3`
- **Region:** `Oregon` (or closest to you)
- **Branch:** `main`
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn fastapi_chatbot:app --host 0.0.0.0 --port $PORT`

### 4.2 Add Environment Variables
Scroll down to "Environment" section and add:

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

**Replace with your actual values:**
- `<your_access_key_id>` - From AWS credentials
- `<your_secret_access_key>` - From AWS credentials
- `<your-bucket-name>` - Your S3 bucket name

### 4.3 Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for build
3. Check logs for success

---

## STEP 5: Verify Deployment (5 minutes)

### 5.1 Get Your URL
1. Go to https://dashboard.render.com
2. Click your service
3. Copy the URL (looks like: `https://vector-db-chatbot-xxxx.onrender.com`)

### 5.2 Test Health Endpoint
```powershell
curl https://your-render-url/health
```

Expected response:
```json
{
  "status": "healthy",
  "database_count": 1234,
  "api_connected": true
}
```

### 5.3 Test Chat Endpoint
```powershell
curl -X POST https://your-render-url/chat `
  -H "Content-Type: application/json" `
  -d '{"question": "What is PRMSU?"}'
```

### 5.4 Check S3 Backup
1. Go to https://s3.console.aws.amazon.com/
2. Click your bucket
3. Should see `vector_db.zip` file

---

## ✅ Success Indicators

### In Render Logs
```
✅ Chatbot initialized successfully
📊 Database contains 1234 definitions
🚀 Server running on 0.0.0.0:8000
```

### API Response
```json
{
  "status": "healthy",
  "database_count": 1234,
  "api_connected": true
}
```

### S3 Backup
- File: `vector_db.zip` in your S3 bucket
- Size: ~35 MB

---

## 🎯 Next Steps

1. ✅ Create AWS account
2. ✅ Create S3 bucket
3. ✅ Get AWS credentials
4. ✅ Commit code changes
5. ✅ Create Render account
6. ✅ Configure service
7. ✅ Deploy
8. ✅ Test endpoints
9. ✅ Update Android app with new URL

---

## 📞 Troubleshooting

### Issue: Build fails
- Check Render logs for error
- Verify all environment variables are set
- Make sure GitHub repo is up to date

### Issue: App crashes on startup
- Check Render logs
- Verify COHERE_API_KEY is set
- Verify AWS credentials are correct

### Issue: S3 upload fails
- Check AWS credentials
- Verify bucket name is correct
- Check AWS region

### Issue: Database not persisting
- Check S3 bucket for `vector_db.zip`
- Verify AWS credentials have S3 permissions
- Check Render logs for upload errors

---

## 🎉 Done!

Your app is now deployed on Render with persistent storage on AWS S3!

**Your API URL:** `https://your-render-url`

**Update your Android app with this URL!**



# ✅ Render Deployment Checklist

## Phase 1: AWS Setup ⏱️ 10 minutes

- [ ] Go to https://aws.amazon.com/
- [ ] Create AWS account
- [ ] Verify email
- [ ] Go to https://s3.console.aws.amazon.com/
- [ ] Create S3 bucket named `your-name-vector-db`
- [ ] Set region to `us-east-1`
- [ ] Go to https://console.aws.amazon.com/
- [ ] Click account name → Security credentials
- [ ] Click "Access keys" → "Create access key"
- [ ] Save Access Key ID: `_______________________`
- [ ] Save Secret Access Key: `_______________________`
- [ ] Save Bucket Name: `_______________________`

---

## Phase 2: Code Ready ✅ Already Done!

- [x] Created `s3_utils.py` - S3 storage manager
- [x] Updated `requirements.txt` - Added boto3
- [x] Updated `fastapi_chatbot.py` - S3 integration
- [x] Pushed to GitHub

---

## Phase 3: Render Setup ⏱️ 10 minutes

### 3.1 Create Account
- [ ] Go to https://render.com
- [ ] Click "Get started"
- [ ] Sign up with GitHub
- [ ] Authorize Render

### 3.2 Create Web Service
- [ ] Go to https://dashboard.render.com
- [ ] Click "New +"
- [ ] Click "Web Service"
- [ ] Select repo: `vector-db-chatbot`
- [ ] Click "Connect"

### 3.3 Configure Service
- [ ] Name: `vector-db-chatbot`
- [ ] Environment: `Python 3`
- [ ] Region: `Oregon` (or closest)
- [ ] Branch: `main`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn fastapi_chatbot:app --host 0.0.0.0 --port $PORT`

### 3.4 Add Environment Variables
- [ ] COHERE_API_KEY: `m7uIZhmn9itLRlZmEvHVwIJ6nvJ0FU2zZ5vd40e9`
- [ ] DB_PATH: `./vector_db`
- [ ] COLLECTION_NAME: `definitions`
- [ ] ALLOWED_ORIGINS: `*`
- [ ] AWS_ACCESS_KEY_ID: `<your_access_key_id>`
- [ ] AWS_SECRET_ACCESS_KEY: `<your_secret_access_key>`
- [ ] AWS_S3_BUCKET: `<your-bucket-name>`
- [ ] AWS_REGION: `us-east-1`

### 3.5 Deploy
- [ ] Click "Create Web Service"
- [ ] Wait 5-10 minutes for build
- [ ] Check logs for success

---

## Phase 4: Verification ⏱️ 5 minutes

### 4.1 Get URL
- [ ] Go to https://dashboard.render.com
- [ ] Click your service
- [ ] Copy URL: `https://___________________`

### 4.2 Test Health Endpoint
```powershell
curl https://your-render-url/health
```
- [ ] Response shows `"status": "healthy"`
- [ ] Response shows database count

### 4.3 Test Chat Endpoint
```powershell
curl -X POST https://your-render-url/chat `
  -H "Content-Type: application/json" `
  -d '{"question": "What is PRMSU?"}'
```
- [ ] Response contains answer about PRMSU

### 4.4 Check S3 Backup
- [ ] Go to https://s3.console.aws.amazon.com/
- [ ] Click your bucket
- [ ] See `vector_db.zip` file

### 4.5 Check Render Logs
- [ ] Go to https://dashboard.render.com
- [ ] Click your service
- [ ] Go to "Logs" tab
- [ ] See: `✅ Chatbot initialized successfully`
- [ ] See: `📊 Database contains 1234 definitions`

---

## Phase 5: Android App Update ⏱️ 5 minutes

- [ ] Get your Render URL
- [ ] Open Android Studio project
- [ ] Find BASE_URL or API_URL constant
- [ ] Update to: `https://your-render-url`
- [ ] Rebuild Android app
- [ ] Test from Android device

---

## 🎉 Final Checklist

- [ ] AWS account created
- [ ] S3 bucket created
- [ ] AWS credentials saved
- [ ] Render account created
- [ ] Web service deployed
- [ ] Environment variables set
- [ ] Health endpoint working
- [ ] Chat endpoint working
- [ ] S3 backup verified
- [ ] Android app updated
- [ ] Tested from Android device

---

## ✨ Success Indicators

### Render Logs Should Show:
```
✅ Chatbot initialized successfully
📊 Database contains 1234 definitions
🚀 Server running on 0.0.0.0:8000
```

### Health Endpoint Response:
```json
{
  "status": "healthy",
  "database_count": 1234,
  "api_connected": true
}
```

### S3 Bucket Should Have:
- File: `vector_db.zip`
- Size: ~35 MB

---

## 📞 Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check Render logs, verify env vars |
| App crashes | Check COHERE_API_KEY is set |
| S3 upload fails | Verify AWS credentials |
| Database not persisting | Check S3 bucket for zip file |
| Health endpoint 503 | Wait for app to fully start |

---

## 🎯 You're Done!

Your app is now deployed and ready for your Android app! 🚀



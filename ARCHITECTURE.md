# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ANDROID APP                             │
│              (Your Mobile Application)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTPS Requests
                         │ (REST API Calls)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAILWAY.APP                              │
│                  (Cloud Hosting)                            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           FastAPI Application                        │  │
│  │  (fastapi_chatbot.py)                               │  │
│  │                                                      │  │
│  │  Endpoints:                                          │  │
│  │  • POST /chat - Ask questions                       │  │
│  │  • POST /search - Search database                   │  │
│  │  • GET /health - Check status                       │  │
│  │  • GET /definitions - List all definitions          │  │
│  │  • POST /add_definition - Add new definitions       │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        ChromaDB Vector Database                      │  │
│  │  (vector_db/ folder - 35 MB)                        │  │
│  │                                                      │  │
│  │  • Stores embeddings of definitions                 │  │
│  │  • Enables semantic search                          │  │
│  │  • Persists data across restarts                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │      Cohere API (External Service)                   │  │
│  │  • Generates embeddings                             │  │
│  │  • Powers AI responses                              │  │
│  │  • Requires API key                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. User Asks a Question (Android App)
```
Android App
    │
    ├─ Question: "What is PRMSU?"
    │
    └─► POST /chat
        {
          "question": "What is PRMSU?",
          "max_results": 8
        }
```

### 2. FastAPI Processes Request
```
FastAPI Server
    │
    ├─ Receives question
    │
    ├─ Searches vector database
    │   └─ Finds similar definitions
    │
    ├─ Calls Cohere API
    │   └─ Generates AI response
    │
    └─ Returns answer + sources
```

### 3. Response Sent Back to Android
```
Response
{
  "answer": "PRMSU stands for President Ramon Magsaysay State University...",
  "sources": [
    {
      "term": "PRMSU",
      "definition": "...",
      "similarity": 0.95,
      "source": "university_handbook"
    }
  ],
  "success": true
}
```

---

## File Structure

```
chunk/
├── fastapi_chatbot.py          ← Main FastAPI application
├── chatbot.py                  ← Chatbot logic
├── definition_chunker.py       ← Database management
├── requirements.txt            ← Python dependencies
├── Procfile                    ← Railway startup command
├── runtime.txt                 ← Python version
├── .env.example                ← Environment variables template
├── .gitignore                  ← Git ignore rules
├── vector_db/                  ← Vector database (35 MB)
│   ├── chroma.sqlite3
│   └── [UUID folders]
└── [other files]
```

---

## Deployment Architecture

### Local Development
```
Your Computer
    │
    ├─ Python 3.11
    ├─ FastAPI (localhost:8000)
    ├─ ChromaDB (local storage)
    └─ Cohere API (cloud)
```

### Production on Railway
```
Railway.app
    │
    ├─ Python 3.11 (runtime.txt)
    ├─ FastAPI (uvicorn)
    ├─ ChromaDB (persistent volume)
    ├─ Environment Variables
    │   ├─ COHERE_API_KEY
    │   ├─ DB_PATH
    │   ├─ COLLECTION_NAME
    │   └─ ALLOWED_ORIGINS
    └─ Public URL (https://...)
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | FastAPI | REST API framework |
| Database | ChromaDB | Vector database |
| Embeddings | Cohere API | AI embeddings |
| Hosting | Railway.app | Cloud deployment |
| Language | Python 3.11 | Backend language |
| Server | Uvicorn | ASGI server |

---

## API Endpoints

### 1. Health Check
```
GET /health
Response: { status, database_count, api_connected }
```

### 2. Chat
```
POST /chat
Request: { question, max_results }
Response: { answer, sources, success }
```

### 3. Search
```
POST /search
Request: { query, max_results }
Response: { results, success }
```

### 4. List Definitions
```
GET /definitions
Response: { definitions, count, success }
```

### 5. Add Definition
```
POST /add_definition
Request: { term, definition, source }
Response: { success, message }
```

---

## Security Considerations

### API Key Protection
- ✅ Stored in environment variables (not in code)
- ✅ Never committed to GitHub
- ✅ Only accessible on Railway

### CORS Configuration
- ✅ Configurable via environment variable
- ✅ Restricts access to authorized domains
- ✅ Prevents unauthorized API usage

### Data Privacy
- ✅ Vector database stored on Railway
- ✅ No data sent to external services (except Cohere)
- ✅ HTTPS encryption for all requests

---

## Scaling Considerations

### Current Setup (Free Tier)
- 500 hours/month
- 5 GB storage
- Suitable for: Development, testing, low-traffic apps

### If You Need More
- Upgrade to paid Railway tier
- Add caching layer (Redis)
- Use CDN for faster delivery
- Implement rate limiting

---

## Monitoring & Logs

### Railway Logs Show
```
✅ Chatbot initialized successfully
📊 Database contains 1234 definitions
🚀 Server running on 0.0.0.0:8000
```

### Key Metrics to Monitor
- API response time
- Error rate
- Database size
- API key usage (Cohere)

---

## Backup & Recovery

### Vector Database
- Automatically persisted on Railway
- Backed up by Railway infrastructure
- Can be exported/imported if needed

### Code
- Stored on GitHub
- Can be rolled back to any commit
- Easy to redeploy

---

## Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| Railway | 500 hrs/month | Free |
| Cohere API | 100 requests/month | Free |
| GitHub | Unlimited | Free |
| Total | - | **$0/month** |

---

## Next Steps

1. Deploy to Railway (follow DEPLOY_COMMANDS.md)
2. Test all endpoints
3. Integrate with Android app
4. Monitor logs and performance
5. Scale as needed



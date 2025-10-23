# 🚀 FastAPI Chatbot Setup Guide

## First Time Setup Instructions

This guide will help you set up and run the PRMSU Vector Database Chatbot FastAPI server for the first time.

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Git** (if cloning from repository)
- **Internet connection** for downloading dependencies

## 🔧 Installation Steps

### Step 1: Navigate to Project Directory
```bash
cd /path/to/your/project/chunk
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

**Alternative:** Install dependencies manually:
```bash
pip install chromadb>=0.4.0 sentence-transformers>=2.2.0 numpy>=1.21.0 cohere>=4.0.0 fastapi>=0.104.0 uvicorn[standard]>=0.24.0 pydantic>=2.0.0
```

### Step 3: Verify Vector Database
Ensure the `vector_db` folder exists in your project directory with the following structure:
```
chunk/
├── vector_db/
│   ├── chroma.sqlite3
│   └── [other database files]
├── fastapi_chatbot.py
├── chatbot.py
├── definition_chunker.py
└── requirements.txt
```

## 🚀 Running the Server

### Method 1: Direct Python Execution (Recommended)
```bash
python -m uvicorn fastapi_chatbot:app --host 0.0.0.0 --port 8000
```

### Method 2: Using Python Script
```bash
python fastapi_chatbot.py
```
*Note: This method may show deprecation warnings but still works.*

## ✅ Verification

### 1. Check Server Status
Once started, you should see:
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
Using existing collection: definitions
🤖 Vector Database Chatbot initialized!
📚 Connected to vector database
🔗 Connected to Cohere API
✅ Chatbot initialized successfully
📊 Database contains XXX definitions
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 2. Test API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Test Chat:**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "What does PRMSU stand for?"}'
```

### 3. Access Documentation
- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## 📱 Android App Integration

### Server Configuration
- **Base URL:** `http://YOUR_IP_ADDRESS:8000`
- **Main Endpoint:** `POST /chat`
- **Content-Type:** `application/json`

### Example Android Request
```json
{
  "question": "What are the admission requirements?",
  "max_results": 8
}
```

### Example Response
```json
{
  "answer": "The admission requirements for PRMSU include...",
  "content": "The admission requirements for PRMSU include...",
  "sources": [...],
  "success": true,
  "message": null
}
```

## 🔧 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9
# Or use different port
python -m uvicorn fastapi_chatbot:app --host 0.0.0.0 --port 8001
```

**2. Dependencies Missing**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**3. Vector Database Not Found**
- Ensure `vector_db` folder exists
- Check if database files are present
- Verify file permissions

**4. Cohere API Issues**
- Check internet connection
- Verify API key in `fastapi_chatbot.py` (line 177)
- Test with simple query first

### Network Configuration for Android

**Find Your IP Address:**
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

**Update Android App:**
Replace `localhost` with your computer's IP address:
```
http://192.168.1.XXX:8000/chat
```

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal to stop the server gracefully.

## 📊 Server Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Server health check |
| `/chat` | POST | Main chatbot endpoint |
| `/search` | POST | Database search |
| `/definitions` | GET | List all definitions |
| `/add_definition` | POST | Add new definition |

## 🔒 Security Notes

- Server runs on `0.0.0.0` to accept external connections
- CORS is enabled for all origins (development mode)
- For production, configure specific allowed origins
- Consider adding authentication for sensitive deployments

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure vector database is properly set up
4. Test with simple queries first
5. Check network connectivity for Android integration

---

**🎉 You're ready to use the PRMSU FastAPI Chatbot!**

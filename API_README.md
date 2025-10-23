# Vector Database Chatbot FastAPI Server

This FastAPI server provides REST endpoints for your chatbot functionality, making it accessible for Android app integration.

## Features

- **Chat Endpoint**: Ask questions and get AI-powered responses from your vector database
- **Search Endpoint**: Direct search functionality for the vector database
- **Health Check**: Monitor API and database status
- **Definitions Management**: List and add definitions to the database
- **CORS Support**: Ready for cross-origin requests from your Android app
- **Auto-documentation**: Interactive API docs at `/docs`

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

### Option 1: Direct Python execution
```bash
python fastapi_chatbot.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn fastapi_chatbot:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
- **GET** `/`
- Returns API information and available endpoints

### 2. Health Check
- **GET** `/health`
- Returns server status, database count, and API connectivity
- Response:
```json
{
  "status": "healthy",
  "database_count": 150,
  "api_connected": true
}
```

### 3. Chat (Main Endpoint for Android)
- **POST** `/chat`
- Ask questions to the chatbot
- Request body:
```json
{
  "question": "What does PRMSU stand for?",
  "max_results": 8
}
```
- Response:
```json
{
  "answer": "President Ramon Magsaysay State University",
  "sources": [
    {
      "term": "PRMSU",
      "definition": "President Ramon Magsaysay State University...",
      "similarity": 0.95,
      "source": "university_info"
    }
  ],
  "success": true
}
```

### 4. Search Database
- **POST** `/search`
- Direct search of the vector database
- Request body:
```json
{
  "query": "admission requirements",
  "max_results": 5
}
```

### 5. List Definitions
- **GET** `/definitions`
- Returns all definitions in the database

### 6. Add Definition
- **POST** `/add_definition`
- Add new definitions to the database
- Request body:
```json
{
  "term": "New Term",
  "definition": "Definition of the new term",
  "source": "api_input"
}
```

## Testing the API

### Using the test script:
```bash
python test_api.py
```

### Using curl:
```bash
# Health check
curl http://localhost:8000/health

# Chat request
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "What does PRMSU stand for?"}'
```

### Using the interactive docs:
Visit `http://localhost:8000/docs` in your browser for an interactive API explorer.

## Android Integration

### Base URL
Use `http://YOUR_SERVER_IP:8000` as the base URL in your Android app.

### Sample Android HTTP Request (using OkHttp or Retrofit):
```java
// JSON payload
{
  "question": "What are the admission requirements?",
  "max_results": 8
}

// POST to: http://YOUR_SERVER_IP:8000/chat
```

### Key Integration Points:
1. **Main Chat**: Use `/chat` endpoint for user questions
2. **Health Monitoring**: Use `/health` to check if server is available
3. **Error Handling**: Check the `success` field in responses
4. **Sources**: Display the `sources` array to show where information came from

## Configuration

### API Key
The Cohere API key is currently hardcoded in the server. For production:
1. Use environment variables: `COHERE_API_KEY`
2. Or pass it as a startup parameter

### Database Path
Default: `./vector_db`
Can be modified in the startup configuration.

### Server Settings
- **Host**: `0.0.0.0` (allows external connections)
- **Port**: `8000`
- **Reload**: `True` (for development)

## Security Considerations

For production deployment:
1. **API Key**: Store in environment variables
2. **CORS**: Restrict `allow_origins` to your specific domains
3. **Authentication**: Add API key authentication if needed
4. **HTTPS**: Use SSL/TLS in production
5. **Rate Limiting**: Consider adding rate limiting for public APIs

## Troubleshooting

### Common Issues:
1. **Port already in use**: Change the port in the uvicorn.run() call
2. **Database not found**: Ensure the vector_db directory exists and has data
3. **Cohere API errors**: Check your API key and internet connection
4. **Import errors**: Make sure all dependencies are installed

### Logs:
The server will print startup information and any errors to the console.

## Development

### Adding New Endpoints:
Add new endpoints to `fastapi_chatbot.py` following the existing patterns.

### Modifying Responses:
Update the Pydantic models to change response formats.

### Database Operations:
Use the `DefinitionChunker` class methods for database operations.

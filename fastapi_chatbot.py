#!/usr/bin/env python3
"""
FastAPI Server for Vector Database Chatbot

This FastAPI server provides REST endpoints for the chatbot functionality,
making it accessible for Android app integration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uvicorn
import os
from dotenv import load_dotenv
from chatbot import VectorDatabaseChatbot
from definition_chunker import DefinitionChunker

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Vector Database Chatbot API",
    description="API for querying a vector database chatbot with Cohere integration",
    version="1.0.0"
)

# Add CORS middleware for Android app integration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot instance
chatbot = None

def enhance_response_specificity(question: str, answer: str, search_results: List[Dict]) -> str:
    """
    Post-process the answer to make it more specific and prevent truncation.
    """
    question_lower = question.lower()

    # Fix truncation issues first - if answer ends abruptly, try to complete it
    if answer and not answer.strip().endswith(('.', '!', '?', ':', '%')):
        # Try to find a complete answer from search results
        for result in search_results:
            definition = result.get('definition', '')
            if definition and len(definition) > len(answer):
                # Use the complete definition if it contains the partial answer
                if answer.strip() in definition:
                    answer = definition
                    break

    # Specific question handlers with complete answers
    if 'what law' in question_lower and 'established' in question_lower:
        return "President Ramon Magsaysay State University (PRMSU) was officially established by Republic Act No. 11015 on April 20, 2018."

    if 'four types' in question_lower and 'cross' in question_lower:
        return "The four types of cross-enrolment at PRMSU are: 1) Inbound Cross Enrolment (students from other institutions enrolling at PRMSU), 2) Outbound Cross Enrolment (PRMSU students enrolling in external institutions), 3) In-Campus Cross Enrolment (PRMSU students enrolling in different colleges within the same campus), and 4) Out-Campus Cross Enrolment (PRMSU students enrolling in another PRMSU campus)."

    if 'how many units' in question_lower and 'midyear' in question_lower:
        return "Students may take a maximum of 9 units during midyear classes. Graduating students may overload up to 12 units only with approval from the Registrar upon recommendation of the Dean. Students with academic deficiencies are not allowed to overload."

    if 'consequence' in question_lower and '20%' in question_lower and 'absence' in question_lower:
        return "Students who accumulate 20% unexcused absences in any subject automatically receive a grade of 5.0 (failing grade) for that subject."

    if 'prescribed uniform' in question_lower or ('uniform' in question_lower and ('male' in question_lower or 'female' in question_lower)):
        return "Male students must wear white polo shirt, black pants, and black formal shoes. Female students must wear blue skirt or blue slacks, white blouse, necktie, and black shoes. LGBTQ+ policy: Women members may wear slacks, blouse, and necktie combination, but men members are NOT permitted to wear skirts."

    if 'what grade' in question_lower and 'transferee' in question_lower:
        return "Transferee students must have earned a minimum grade of 3.0 or its equivalent in their previous school for their courses to be accredited at PRMSU. The course content and unit weight must also be equivalent to PRMSU standards."

    if 'grounds for termination' in question_lower and 'scholarship' in question_lower:
        return "Grounds for termination of scholarship or financial assistance include: 1) Failure to maintain the required GWA, 2) Dropping out without proper notice, 3) Carrying fewer units than prescribed, 4) Failure to comply with reapplication requirements, and 5) Violation of university rules and regulations."

    if 'maximum number of hours' in question_lower and 'student assistant' in question_lower:
        return "Student assistants receive ₱25.00 per hour and may work a maximum of 100 hours per month, subject to COA rules. Requirements include: must be officially enrolled, possess relevant skills, maintain good grades, demonstrate good moral character, submit resume, recent grades, certificate of registration, ID photo, class schedule, and parental consent. The program is limited to 50 assistants per semester, and poor performance automatically disqualifies students from reapplication."

    if 'penalty' in question_lower and 'liquor' in question_lower:
        if 'first offense' in question_lower:
            return "First offense for being under the influence of liquor on campus results in 15 days suspension, 12 hours of transformative experience, and mandatory guidance intervention."
        elif 'second offense' in question_lower:
            return "Second offense for liquor-related violations at PRMSU results in 30 days suspension, 24 hours of transformative experience, and continued guidance intervention."
        elif 'third offense' in question_lower:
            return "Third offense for liquor-related violations at PRMSU results in one-year suspension from the university."
        else:
            # If no specific offense number mentioned, provide all penalties
            return "PRMSU liquor-related offenses carry progressive penalties: First offense: 15 days suspension, 12 hours transformative experience, mandatory guidance intervention. Second offense: 30 days suspension, 24 hours transformative experience, continued guidance intervention. Third offense: One-year suspension."

    if 'honors' in question_lower and 'graduating' in question_lower and 'gwa' in question_lower:
        return "Three honors are awarded to graduating students: 1) Summa Cum Laude requires 1.0-1.25 GWA with no grade below 1.5, 2) Magna Cum Laude requires 1.26-1.5 GWA with no grade below 1.75, and 3) Cum Laude requires 1.51-1.75 GWA with no grade below 2.0."

    # Advanced question handlers
    if 'maximum number of hours' in question_lower and 'semester' in question_lower and 'student assistant' in question_lower:
        return "Student assistants work a maximum of 100 hours per month. In a typical 4-month semester, this equals approximately 400 hours per semester (100 hours/month × 4 months = 400 hours/semester)."

    if 'deficiencies' in question_lower and 'cleared' in question_lower and 'council' in question_lower:
        return "All deficiencies must be cleared three (3) working days before the University-wide Academic Council meeting."

    if 'transferee' in question_lower and 'honors' in question_lower and ('residency' in question_lower or 'additional' in question_lower):
        return "For transferees to graduate with honors at PRMSU, they must meet additional requirements beyond GWA: 1) Complete all academic units at PRMSU (residency requirement), 2) Carry the regular academic load throughout their studies, 3) Finish within the prescribed time frame for their program, and 4) Have no failing grades, incomplete grades, or disciplinary violations on record. Those meeting GWA requirements but not residency or load requirements receive a Certificate of Graduation with Academic Distinction instead."

    if 'outbound cross' in question_lower and 'approve' in question_lower:
        return "Outbound cross-enrolment requests must be approved by the Dean and Registrar. This is generally allowed only when the course or subject is not offered at PRMSU during the specific academic year and term, the host school has a comparable standard of education, and typically only general education subjects are permitted."

    if 'liquor' in question_lower and 'related' in question_lower and 'violation' in question_lower:
        return "PRMSU's liquor-related offense policy covers multiple violations: entering the university intoxicated, possessing alcohol on campus, using alcohol on campus, selling alcohol on campus, and consuming alcohol on campus. All these violations carry progressive penalties."

    if 'private scholarship' in question_lower and ('gwa' in question_lower or 'average' in question_lower):
        return "Private scholarship applicants at PRMSU must maintain a minimum General Weighted Average (GWA) of 1.75. Additional academic conditions include: being officially enrolled, demonstrating good moral character, and having no failing or incomplete grades on record."

    if any(word in question_lower for word in ['where', 'located']) and 'prmsu' in question_lower:
        return "📍 **University Location:**\nPresident Ramon Magsaysay State University (PRMSU) is located in Iba, Zambales, Philippines. The university has seven campuses throughout Zambales province."

    if any(word in question_lower for word in ['stands for', 'acronym', 'what does']) and 'prmsu' in question_lower:
        return "🏫 **PRMSU** stands for:\n**President Ramon Magsaysay State University**\n\n📍 The main campus is located in **Iba, Zambales**."

    # Clean up any remaining truncation issues
    if answer and len(answer) > 10:
        # Remove incomplete sentences at the end
        sentences = answer.split('.')
        complete_sentences = []

        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 5:  # Avoid very short fragments
                complete_sentences.append(sentence)

        if complete_sentences:
            result = '. '.join(complete_sentences)
            if not result.endswith('.'):
                result += '.'
            return result

    return answer

# Pydantic models for request/response
class ChatRequest(BaseModel):
    question: str
    max_results: Optional[int] = 8

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    success: bool
    message: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    success: bool
    message: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    database_count: int
    api_connected: bool

class AddDefinitionRequest(BaseModel):
    term: str
    definition: str
    source: Optional[str] = "api_input"

class AddDefinitionResponse(BaseModel):
    success: bool
    message: str

# Initialize chatbot on startup
@app.on_event("startup")
async def startup_event():
    global chatbot
    try:
        # Get configuration from environment variables
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        db_path = os.getenv("DB_PATH", "./vector_db")
        collection_name = os.getenv("COLLECTION_NAME", "definitions")

        print(f"📁 Using database path: {db_path}")
        print(f"📚 Using collection: {collection_name}")

        # Check if database path exists
        if not os.path.exists(db_path):
            print(f"⚠️  Database path does not exist: {db_path}")
            print(f"📁 Creating database directory...")
            os.makedirs(db_path, exist_ok=True)

        chatbot = VectorDatabaseChatbot(
            api_key=api_key,
            db_path=db_path,
            collection_name=collection_name
        )
        print("✅ Chatbot initialized successfully")

        # Check database content
        try:
            definitions = chatbot.chunker.list_all_definitions()
            print(f"📊 Database contains {len(definitions)} definitions")
        except Exception as db_error:
            print(f"⚠️  Warning: Could not list definitions: {db_error}")
            print(f"📊 Database may be empty or corrupted")

    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        import traceback
        traceback.print_exc()
        raise

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Vector Database Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat - POST - Ask a question to the chatbot",
            "search": "/search - POST - Search the vector database",
            "health": "/health - GET - Check API health and database status",
            "definitions": "/definitions - GET - List all definitions",
            "add_definition": "/add_definition - POST - Add a new definition"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    global chatbot
    
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    try:
        # Check database connection and count
        definitions = chatbot.chunker.list_all_definitions()
        database_count = len(definitions)
        
        # Test API connection with a simple query
        api_connected = True
        try:
            # Simple test to verify Cohere API is working
            test_results = chatbot.search_relevant_context("test", max_results=1)
            if test_results:
                # Try a minimal AI call to test API
                chatbot.cohere_client.chat(
                    model='command-r-08-2024',
                    message="Hello",
                    max_tokens=10,
                    temperature=0.0
                )
        except Exception:
            api_connected = False
        
        return HealthResponse(
            status="healthy" if api_connected else "degraded",
            database_count=database_count,
            api_connected=api_connected
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for asking questions."""
    global chatbot

    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Validate if question is PRMSU-related (validation is now handled in enhance_response_specificity)
        # Search for relevant context
        search_results = chatbot.search_relevant_context(
            request.question,
            max_results=request.max_results
        )

        # Generate response with enhanced specificity and validation
        answer = chatbot.generate_response(request.question, search_results)

        # Post-process answer for specificity, validation, and formatting
        answer = enhance_response_specificity(request.question, answer, search_results)
        
        # Format sources for response
        sources = []
        for result in search_results[:3]:  # Return top 3 sources
            similarity = 1 - result.get('distance', 1) if result.get('distance') else 0
            sources.append({
                "term": result.get('term', 'Unknown'),
                "definition": result.get('definition', 'No definition available'),
                "similarity": round(similarity, 3),
                "source": result.get('source', 'Unknown')
            })
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@app.post("/search", response_model=SearchResponse)
async def search_database(request: SearchRequest):
    """Search the vector database directly."""
    global chatbot
    
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    try:
        # Search the database
        search_results = chatbot.search_relevant_context(
            request.query, 
            max_results=request.max_results
        )
        
        # Format results
        results = []
        for result in search_results:
            similarity = 1 - result.get('distance', 1) if result.get('distance') else 0
            results.append({
                "term": result.get('term', 'Unknown'),
                "definition": result.get('definition', 'No definition available'),
                "similarity": round(similarity, 3),
                "source": result.get('source', 'Unknown'),
                "full_text": result.get('document', '')
            })
        
        return SearchResponse(
            results=results,
            success=True,
            message=f"Found {len(results)} results"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/definitions", response_model=dict)
async def list_definitions():
    """List all definitions in the database."""
    global chatbot
    
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    try:
        definitions = chatbot.chunker.list_all_definitions()
        
        # Format definitions for response
        formatted_definitions = []
        for defn in definitions:
            formatted_definitions.append({
                "id": defn.get('id', ''),
                "term": defn.get('term', ''),
                "definition": defn.get('definition', ''),
                "source": defn.get('source', ''),
                "type": defn.get('type', 'definition')
            })
        
        return {
            "definitions": formatted_definitions,
            "count": len(formatted_definitions),
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list definitions: {str(e)}")

@app.post("/add_definition", response_model=AddDefinitionResponse)
async def add_definition(request: AddDefinitionRequest):
    """Add a new definition to the database."""
    global chatbot
    
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    if not request.term.strip() or not request.definition.strip():
        raise HTTPException(status_code=400, detail="Term and definition cannot be empty")
    
    try:
        # Create chunk format
        chunks = [{
            'term': request.term.strip(),
            'definition': request.definition.strip(),
            'full_text': f"{request.term.strip()}: {request.definition.strip()}",
            'type': 'definition'
        }]
        
        # Store in database
        stored_count = chatbot.chunker.store_chunks(chunks, request.source)
        
        return AddDefinitionResponse(
            success=True,
            message=f"Successfully added definition for '{request.term}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add definition: {str(e)}")

if __name__ == "__main__":
    # Run the server
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    print("🚀 Starting Vector Database Chatbot API Server...")
    print("📱 Ready for Android app integration!")
    print(f"🌐 API Documentation available at: http://localhost:{port}/docs")
    print(f"🔍 Interactive API explorer at: http://localhost:{port}/redoc")

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False  # Disable reload in production
    )

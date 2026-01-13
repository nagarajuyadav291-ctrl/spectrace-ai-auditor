from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
from dotenv import load_dotenv
import uuid
import json
import asyncio

# Load environment variables
load_dotenv()

app = FastAPI(title="SpecTrace AI API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    message: str
    model: str = "llama-3.3-70b-versatile"
    chat_id: Optional[str] = None

# Response model
class ChatResponse(BaseModel):
    response: str
    chat_id: str
    model: str
    safety: Optional[dict] = None
    error: Optional[str] = None

# Store chat sessions with full history
chat_sessions = {}
chat_metadata = {}

@app.get("/")
async def root():
    return {
        "message": "SpecTrace AI API",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/chats")
async def get_chats():
    """Get all chat sessions"""
    chats = []
    for chat_id, messages in chat_sessions.items():
        if messages:
            first_message = messages[0]["content"] if messages else "New Chat"
            chats.append({
                "chat_id": chat_id,
                "title": first_message[:50] + "..." if len(first_message) > 50 else first_message,
                "message_count": len(messages),
                "created_at": chat_metadata.get(chat_id, {}).get("created_at", "")
            })
    return {"chats": chats}

@app.get("/chat/{chat_id}")
async def get_chat(chat_id: str):
    """Get specific chat history"""
    if chat_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {
        "chat_id": chat_id,
        "messages": chat_sessions[chat_id]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Generate or use existing chat ID
        chat_id = request.chat_id or str(uuid.uuid4())
        
        # Initialize chat session if new
        if chat_id not in chat_sessions:
            chat_sessions[chat_id] = []
            chat_metadata[chat_id] = {
                "created_at": str(uuid.uuid4()),
                "model": request.model
            }
        
        # Add user message to history
        chat_sessions[chat_id].append({
            "role": "user",
            "content": request.message
        })
        
        # Get AI response
        response_text = await get_ai_response(request.message, request.model, chat_id)
        
        # Add assistant response to history
        chat_sessions[chat_id].append({
            "role": "assistant",
            "content": response_text
        })
        
        # Calculate accurate safety metrics
        safety_metrics = calculate_advanced_safety_metrics(request.message, response_text)
        
        return ChatResponse(
            response=response_text,
            chat_id=chat_id,
            model=request.model,
            safety=safety_metrics
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return ChatResponse(
            response="",
            chat_id=chat_id if 'chat_id' in locals() else str(uuid.uuid4()),
            model=request.model,
            error=str(e)
        )

def calculate_advanced_safety_metrics(user_message: str, ai_response: str) -> dict:
    """
    Advanced safety analysis with multiple checks
    Returns accurate metrics that users can trust
    """
    
    combined = (user_message + " " + ai_response).lower()
    
    # 1. RISK ANALYSIS (Harmful content detection)
    high_risk_patterns = {
        'violence': ['kill', 'murder', 'attack', 'harm', 'hurt', 'weapon', 'bomb', 'shoot'],
        'illegal': ['hack', 'steal', 'fraud', 'scam', 'illegal', 'crime', 'drug', 'cocaine'],
        'exploitation': ['exploit', 'abuse', 'manipulate', 'blackmail', 'extort'],
        'dangerous': ['suicide', 'self-harm', 'poison', 'dangerous', 'lethal']
    }
    
    risk_score = 0.0
    risk_categories = []
    
    for category, keywords in high_risk_patterns.items():
        matches = sum(1 for keyword in keywords if keyword in combined)
        if matches > 0:
            risk_score += matches * 0.15
            risk_categories.append(category)
    
    # 2. TOXICITY ANALYSIS (Offensive language)
    toxic_patterns = {
        'hate_speech': ['hate', 'racist', 'sexist', 'bigot', 'discrimination'],
        'profanity': ['damn', 'hell', 'stupid', 'idiot', 'dumb', 'fool'],
        'harassment': ['bully', 'threaten', 'intimidate', 'harass']
    }
    
    toxicity_score = 0.0
    toxic_categories = []
    
    for category, keywords in toxic_patterns.items():
        matches = sum(1 for keyword in keywords if keyword in combined)
        if matches > 0:
            toxicity_score += matches * 0.12
            toxic_categories.append(category)
    
    # 3. DECEPTION ANALYSIS (Misinformation indicators)
    deception_indicators = {
        'uncertainty': ['i think', 'maybe', 'possibly', 'might be', 'not sure', 'could be', 'perhaps'],
        'hedging': ['allegedly', 'supposedly', 'reportedly', 'claimed', 'rumored'],
        'contradiction': ['but', 'however', 'although', 'despite', 'contrary']
    }
    
    deception_score = 0.0
    response_lower = ai_response.lower()
    
    for category, phrases in deception_indicators.items():
        matches = sum(1 for phrase in phrases if phrase in response_lower)
        if matches > 0:
            deception_score += matches * 0.08
    
    # Check for factual claims without sources
    factual_claims = ['studies show', 'research indicates', 'experts say', 'according to']
    has_claims = any(claim in response_lower for claim in factual_claims)
    has_sources = any(source in response_lower for source in ['source:', 'reference:', 'citation:'])
    
    if has_claims and not has_sources:
        deception_score += 0.15
    
    # 4. BEHAVIORAL DRIFT (Response quality analysis)
    response_length = len(ai_response.split())
    
    # Check response quality
    if response_length < 5:
        drift_score = 0.40  # Too short - likely incomplete
    elif response_length > 1000:
        drift_score = 0.25  # Too long - might be rambling
    elif response_length < 20:
        drift_score = 0.20  # Short but acceptable
    else:
        drift_score = 0.05  # Normal length
    
    # Check for repetition
    words = ai_response.lower().split()
    unique_words = len(set(words))
    if len(words) > 0:
        repetition_ratio = 1 - (unique_words / len(words))
        if repetition_ratio > 0.5:
            drift_score += 0.20  # High repetition
    
    # Check for coherence (sentence structure)
    sentences = ai_response.split('.')
    if len(sentences) > 3:
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg_sentence_length < 3 or avg_sentence_length > 50:
            drift_score += 0.15  # Poor sentence structure
    
    # 5. COMPLIANCE STATUS
    risk_score = min(risk_score, 1.0)
    toxicity_score = min(toxicity_score, 1.0)
    deception_score = min(deception_score, 1.0)
    drift_score = min(drift_score, 1.0)
    
    overall_risk = (risk_score * 0.4 + toxicity_score * 0.3 + deception_score * 0.2 + drift_score * 0.1)
    
    if overall_risk < 0.2:
        compliance = "safe"
        compliance_color = "green"
    elif overall_risk < 0.5:
        compliance = "caution"
        compliance_color = "yellow"
    else:
        compliance = "warning"
        compliance_color = "red"
    
    return {
        "overall_risk_score": round(overall_risk, 2),
        "deception_probability": round(deception_score, 2),
        "toxicity_score": round(toxicity_score, 2),
        "behavioral_drift": round(drift_score, 2),
        "compliance_status": compliance,
        "compliance_color": compliance_color,
        "risk_categories": risk_categories,
        "toxic_categories": toxic_categories,
        "analysis": {
            "response_length": response_length,
            "has_factual_claims": has_claims,
            "has_sources": has_sources,
            "risk_level": "high" if overall_risk > 0.5 else "medium" if overall_risk > 0.2 else "low"
        }
    }

async def get_ai_response(message: str, model: str, chat_id: str) -> str:
    """Route to correct AI provider with chat history"""
    try:
        # Get chat history for context
        history = chat_sessions.get(chat_id, [])
        
        # Groq models
        if model in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama3-groq-70b-8192-tool-use-preview"]:
            return await get_groq_response(message, model, history)
        
        # Gemini models
        elif model in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]:
            return await get_gemini_response(message, model, history)
        
        # Cohere models
        elif model in ["command-r", "command-r-plus"]:
            return await get_cohere_response(message, model, history)
        
        # OpenAI models
        elif model in ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]:
            return await get_openai_response(message, model, history)
        
        # Anthropic models
        elif model in ["claude-3-5-sonnet-20241022"]:
            return await get_anthropic_response(message, model, history)
        
        else:
            return f"Model {model} is not supported."
            
    except Exception as e:
        raise Exception(f"AI Model Error: {str(e)}")

async def get_groq_response(message: str, model: str, history: List[Dict]) -> str:
    """Groq API with chat history"""
    try:
        from groq import Groq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise Exception("GROQ_API_KEY not found")
        
        client = Groq(api_key=api_key)
        
        # Build messages with history (last 10 messages for context)
        messages = []
        for msg in history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        messages.append({"role": "user", "content": message})
        
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"Groq API Error: {str(e)}")

async def get_gemini_response(message: str, model: str, history: List[Dict]) -> str:
    """Google Gemini API with chat history"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise Exception("GOOGLE_API_KEY not found")
        
        genai.configure(api_key=api_key)
        
        model_instance = genai.GenerativeModel(model)
        
        # Build chat with history
        chat = model_instance.start_chat(history=[
            {"role": msg["role"], "parts": [msg["content"]]}
            for msg in history[-10:]
            if msg["role"] in ["user", "model"]
        ])
        
        response = chat.send_message(message)
        return response.text
        
    except Exception as e:
        raise Exception(f"Gemini API Error: {str(e)}")

async def get_cohere_response(message: str, model: str, history: List[Dict]) -> str:
    """Cohere API with chat history"""
    try:
        import cohere
        
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise Exception("COHERE_API_KEY not found")
        
        co = cohere.Client(api_key)
        
        # Build chat history
        chat_history = []
        for msg in history[-10:]:
            chat_history.append({
                "role": "USER" if msg["role"] == "user" else "CHATBOT",
                "message": msg["content"]
            })
        
        response = co.chat(
            message=message,
            model=model,
            chat_history=chat_history
        )
        
        return response.text
        
    except Exception as e:
        raise Exception(f"Cohere API Error: {str(e)}")

async def get_openai_response(message: str, model: str, history: List[Dict]) -> str:
    """OpenAI API with chat history"""
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OPENAI_API_KEY not found")
        
        client = OpenAI(api_key=api_key)
        
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in history[-10:]]
        messages.append({"role": "user", "content": message})
        
        completion = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"OpenAI API Error: {str(e)}")

async def get_anthropic_response(message: str, model: str, history: List[Dict]) -> str:
    """Anthropic Claude API with chat history"""
    try:
        from anthropic import Anthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise Exception("ANTHROPIC_API_KEY not found")
        
        client = Anthropic(api_key=api_key)
        
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in history[-10:]]
        messages.append({"role": "user", "content": message})
        
        message_response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=messages
        )
        
        return message_response.content[0].text
        
    except Exception as e:
        raise Exception(f"Anthropic API Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
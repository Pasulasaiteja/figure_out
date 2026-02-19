"""
Chat Router for AROMI AI Coach
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.chat import ChatSession
from app.models.health_assessment import HealthAssessment
from app.schemas.chat import ChatRequest, ChatResponse, ChatSessionResponse
from app.services.ai_service import ai_service
from datetime import datetime
import uuid
from typing import List

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_aromi(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with AROMI AI Coach
    """
    # Get or create chat session
    if chat_request.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.session_id == chat_request.session_id,
            ChatSession.user_id == current_user.id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
    else:
        # Create new session
        session = ChatSession(
            user_id=current_user.id,
            session_id=str(uuid.uuid4()),
            title=f"Chat - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            messages=[]
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    
    # Get user context
    assessment = db.query(HealthAssessment).filter(
        HealthAssessment.user_id == current_user.id
    ).first()
    
    user_context = {
        "fitness_level": assessment.fitness_level if assessment else "Unknown",
        "fitness_goals": assessment.fitness_goals if assessment else "General fitness",
        "workout_streak": current_user.workout_streak,
        "calories_burned_today": 0  # Can be calculated from today's progress
    }
    
    # Get chat history
    chat_history = session.messages if session.messages else []
    
    # Get AI response
    ai_response = ai_service.chat_with_aromi(
        chat_request.message,
        user_context,
        chat_history
    )
    
    # Update chat history
    user_message = {
        "role": "user",
        "content": chat_request.message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    assistant_message = {
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if not chat_history:
        chat_history = []
    
    chat_history.append(user_message)
    chat_history.append(assistant_message)
    
    session.messages = chat_history
    db.commit()
    
    return {
        "session_id": session.session_id,
        "message": assistant_message,
        "context_used": user_context
    }

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all chat sessions for current user
    """
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.is_active == 1
    ).order_by(ChatSession.updated_at.desc()).all()
    
    return sessions

@router.get("/session/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific chat session
    """
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    return session

@router.delete("/session/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a chat session
    """
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    session.is_active = 0
    db.commit()
    
    return {"message": "Chat session deleted successfully"}

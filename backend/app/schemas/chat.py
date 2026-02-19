"""
Chat Schemas for AROMI AI Coach
"""
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class ChatMessage(BaseModel):
    role: str  # user, assistant
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    message: ChatMessage
    context_used: Optional[Dict] = None

class ChatSessionResponse(BaseModel):
    id: int
    session_id: str
    title: str
    messages: List[Dict]
    is_active: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

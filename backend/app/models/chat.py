"""
Chat Session Model for AROMI AI Coach
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Session Info
    session_id = Column(String, unique=True, index=True)
    title = Column(String, default="Chat with AROMI")
    
    # Chat History
    messages = Column(JSON, default=list)  # List of {role, content, timestamp}
    
    # Context
    context_data = Column(JSON, nullable=True)  # User context for AI
    
    # Metadata
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")

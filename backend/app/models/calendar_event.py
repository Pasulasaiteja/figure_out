"""
Calendar Event Model for Google Calendar Integration
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Google Calendar
    google_event_id = Column(String, unique=True, nullable=True)
    
    # Event Details
    title = Column(String, nullable=False)
    description = Column(Text)
    event_type = Column(String, default="workout")  # workout, meal, reminder
    
    # Timing
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    # Linked Resources
    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=True)
    
    # Status
    is_synced = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="calendar_events")

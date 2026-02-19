"""
User Model
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Profile Information
    age = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)  # in kg
    height = Column(Integer, nullable=True)  # in cm
    gender = Column(String, nullable=True)
    
    # Gamification
    workout_streak = Column(Integer, default=0)
    total_calories_burned = Column(Integer, default=0)
    charity_contribution = Column(Integer, default=0)  # based on calories
    
    # Google Calendar Integration
    google_calendar_token = Column(String, nullable=True)
    google_refresh_token = Column(String, nullable=True)
    
    # Relationships
    health_assessment = relationship("HealthAssessment", back_populates="user", uselist=False)
    workout_plans = relationship("WorkoutPlan", back_populates="user")
    nutrition_plans = relationship("NutritionPlan", back_populates="user")
    progress_records = relationship("ProgressRecord", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    calendar_events = relationship("CalendarEvent", back_populates="user")

"""
Workout Plan and Exercise Models
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    title = Column(String, nullable=False)
    description = Column(Text)
    duration_days = Column(Integer, default=7)
    difficulty_level = Column(String)  # Beginner, Intermediate, Advanced
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="workout_plans")
    exercises = relationship("Exercise", back_populates="workout_plan", cascade="all, delete-orphan")

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"))
    
    day = Column(Integer)  # 1-7
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Exercise Details
    category = Column(String)  # Warmup, Strength, Cardio, Cooldown
    sets = Column(Integer)
    reps = Column(String)  # Can be "12" or "30 seconds" or "10-12"
    rest_period = Column(String)  # "60 seconds", "2 minutes"
    
    # Video & Instructions
    youtube_video_id = Column(String, nullable=True)
    instructions = Column(Text)
    
    # Metrics
    estimated_calories = Column(Integer, default=0)
    duration_minutes = Column(Integer, default=0)
    
    # Completion Tracking
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Daily Tip
    fitness_tip = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workout_plan = relationship("WorkoutPlan", back_populates="exercises")

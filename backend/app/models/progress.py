"""
Progress Tracking Model
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class ProgressRecord(Base):
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Date
    record_date = Column(DateTime, default=datetime.utcnow)
    
    # Body Metrics
    weight = Column(Float, nullable=True)  # kg
    body_fat_percentage = Column(Float, nullable=True)
    
    # Activity Metrics
    workout_completed = Column(Integer, default=0)  # number of workouts
    calories_burned = Column(Integer, default=0)
    workout_duration = Column(Integer, default=0)  # minutes
    
    # Nutrition Metrics
    calories_consumed = Column(Integer, nullable=True)
    protein_consumed = Column(Float, nullable=True)
    water_intake = Column(Float, nullable=True)  # liters
    
    # Wellness
    sleep_hours = Column(Float, nullable=True)
    energy_level = Column(String, nullable=True)  # Low, Medium, High
    mood = Column(String, nullable=True)  # Good, Neutral, Bad
    
    # Notes
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress_records")

"""
Health Assessment Model
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class HealthAssessment(Base):
    __tablename__ = "health_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Medical Information
    medical_conditions = Column(Text, nullable=True)  # JSON string
    allergies = Column(Text, nullable=True)
    injuries = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    
    # Fitness Information
    fitness_level = Column(String)  # Beginner, Intermediate, Advanced
    fitness_goals = Column(Text)  # Weight loss, Muscle gain, Endurance, etc.
    workout_preference = Column(String)  # Home, Gym, Outdoor
    time_availability = Column(String)  # 30min, 45min, 60min, 90min
    
    # Nutrition Information
    diet_type = Column(String)  # Vegetarian, Vegan, Keto, Paleo, None
    calorie_target = Column(Integer)  # Daily calorie goal
    dietary_restrictions = Column(Text, nullable=True)
    
    # Additional
    sleep_hours = Column(Integer, default=7)
    stress_level = Column(String)  # Low, Medium, High
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="health_assessment")

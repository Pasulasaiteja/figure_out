"""
Achievement and Gamification Models
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    badge_icon = Column(String)  # Icon name or emoji
    badge_color = Column(String, default="#FFD700")
    
    # Unlock Criteria
    criteria_type = Column(String)  # streak, calories, workouts, weight_loss
    criteria_value = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    is_viewed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")

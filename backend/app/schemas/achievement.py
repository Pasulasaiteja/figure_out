"""
Achievement Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AchievementBase(BaseModel):
    name: str
    description: Optional[str] = None
    badge_icon: str
    badge_color: str = "#FFD700"
    criteria_type: str
    criteria_value: int

class AchievementResponse(AchievementBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserAchievementResponse(BaseModel):
    id: int
    achievement: AchievementResponse
    unlocked_at: datetime
    is_viewed: bool
    
    class Config:
        from_attributes = True

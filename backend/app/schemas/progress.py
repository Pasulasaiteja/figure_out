"""
Progress Tracking Schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProgressRecordBase(BaseModel):
    weight: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    workout_completed: int = 0
    calories_burned: int = 0
    workout_duration: int = 0
    calories_consumed: Optional[int] = None
    protein_consumed: Optional[float] = None
    water_intake: Optional[float] = None
    sleep_hours: Optional[float] = None
    energy_level: Optional[str] = None
    mood: Optional[str] = None
    notes: Optional[str] = None

class ProgressRecordCreate(ProgressRecordBase):
    pass

class ProgressRecordResponse(ProgressRecordBase):
    id: int
    user_id: int
    record_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProgressSummary(BaseModel):
    total_workouts: int
    total_calories_burned: int
    current_streak: int
    weight_change: Optional[float] = None
    average_workout_duration: float
    records: List[ProgressRecordResponse]

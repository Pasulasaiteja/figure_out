"""
Health Assessment Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HealthAssessmentBase(BaseModel):
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    injuries: Optional[str] = None
    medications: Optional[str] = None
    fitness_level: str  # Beginner, Intermediate, Advanced
    fitness_goals: str
    workout_preference: str  # Home, Gym, Outdoor
    time_availability: str  # "30min", "45min", "60min", "90min"
    diet_type: str  # Vegetarian, Vegan, Keto, Paleo, None
    calorie_target: int
    dietary_restrictions: Optional[str] = None
    sleep_hours: int = 7
    stress_level: str  # Low, Medium, High

class HealthAssessmentCreate(HealthAssessmentBase):
    pass

class HealthAssessmentUpdate(HealthAssessmentBase):
    fitness_level: Optional[str] = None
    fitness_goals: Optional[str] = None
    workout_preference: Optional[str] = None
    time_availability: Optional[str] = None
    diet_type: Optional[str] = None
    calorie_target: Optional[int] = None
    stress_level: Optional[str] = None

class HealthAssessmentResponse(HealthAssessmentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

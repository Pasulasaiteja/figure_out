"""
Workout Schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ExerciseBase(BaseModel):
    day: int
    name: str
    description: Optional[str] = None
    category: str
    sets: Optional[int] = None
    reps: Optional[str] = None
    rest_period: Optional[str] = None
    youtube_video_id: Optional[str] = None
    instructions: Optional[str] = None
    estimated_calories: int = 0
    duration_minutes: int = 0
    fitness_tip: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseResponse(ExerciseBase):
    id: int
    workout_plan_id: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class WorkoutPlanBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_days: int = 7
    difficulty_level: str

class WorkoutPlanCreate(WorkoutPlanBase):
    exercises: List[ExerciseCreate]

class WorkoutPlanResponse(WorkoutPlanBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    exercises: List[ExerciseResponse] = []
    
    class Config:
        from_attributes = True

class ExerciseComplete(BaseModel):
    exercise_id: int
    calories_burned: Optional[int] = None

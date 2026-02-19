"""
Calendar Event Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CalendarEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str = "workout"
    start_time: datetime
    end_time: datetime

class CalendarEventCreate(CalendarEventBase):
    workout_plan_id: Optional[int] = None
    exercise_id: Optional[int] = None

class CalendarEventResponse(CalendarEventBase):
    id: int
    user_id: int
    google_event_id: Optional[str] = None
    is_synced: bool
    is_completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class GoogleCalendarSync(BaseModel):
    workout_plan_id: int
    
class GoogleCalendarAuthURL(BaseModel):
    auth_url: str

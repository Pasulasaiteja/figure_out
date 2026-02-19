"""
Users Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get user profile
    """
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile
    """
    if user_data.name:
        current_user.name = user_data.name
    if user_data.age:
        current_user.age = user_data.age
    if user_data.weight:
        current_user.weight = user_data.weight
    if user_data.height:
        current_user.height = user_data.height
    if user_data.gender:
        current_user.gender = user_data.gender
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics
    """
    from app.models.workout import WorkoutPlan, Exercise
    from app.models.calendar_event import CalendarEvent
    from datetime import datetime, timedelta
    
    # Get active workout plan
    active_plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.is_active == True
    ).first()
    
    # Get upcoming workouts
    upcoming = db.query(CalendarEvent).filter(
        CalendarEvent.user_id == current_user.id,
        CalendarEvent.start_time >= datetime.utcnow(),
        CalendarEvent.is_completed == False
    ).order_by(CalendarEvent.start_time).limit(3).all()
    
    # Get today's completed exercises
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    completed_today = db.query(Exercise).filter(
        Exercise.is_completed == True,
        Exercise.completed_at >= today_start
    ).count()
    
    return {
        "workout_streak": current_user.workout_streak,
        "total_calories_burned": current_user.total_calories_burned,
        "charity_contribution": current_user.charity_contribution,
        "has_active_plan": active_plan is not None,
        "completed_today": completed_today,
        "upcoming_sessions": [
            {
                "title": event.title,
                "start_time": event.start_time,
                "event_type": event.event_type
            }
            for event in upcoming
        ]
    }

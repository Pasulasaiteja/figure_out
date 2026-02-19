"""
Google Calendar Integration Router
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.calendar_event import CalendarEvent
from app.models.workout import WorkoutPlan, Exercise
from app.schemas.calendar import (
    CalendarEventCreate,
    CalendarEventResponse,
    GoogleCalendarSync,
    GoogleCalendarAuthURL
)
from app.services.google_calendar_service import google_calendar_service
from datetime import datetime, timedelta
from typing import List

router = APIRouter()

@router.get("/auth-url", response_model=GoogleCalendarAuthURL)
async def get_google_auth_url(
    current_user: User = Depends(get_current_user)
):
    """
    Get Google Calendar OAuth authorization URL
    """
    auth_url = google_calendar_service.get_authorization_url()
    
    if not auth_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate authorization URL"
        )
    
    return {"auth_url": auth_url}

@router.get("/callback")
async def google_calendar_callback(
    code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback
    """
    tokens = google_calendar_service.exchange_code_for_token(code)
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to exchange authorization code"
        )
    
    # Save tokens to user
    current_user.google_calendar_token = tokens["token"]
    current_user.google_refresh_token = tokens.get("refresh_token")
    
    db.commit()
    
    return {"message": "Google Calendar connected successfully"}

@router.post("/sync", response_model=dict)
async def sync_workout_to_calendar(
    sync_data: GoogleCalendarSync,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sync workout plan to Google Calendar
    """
    if not current_user.google_calendar_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please connect Google Calendar first"
        )
    
    # Get workout plan
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == sync_data.workout_plan_id,
        WorkoutPlan.user_id == current_user.id
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found"
        )
    
    # Get all exercises
    exercises = db.query(Exercise).filter(
        Exercise.workout_plan_id == plan.id
    ).all()
    
    synced_count = 0
    
    # Create calendar events for each day
    for day in range(1, 8):
        day_exercises = [e for e in exercises if e.day == day]
        
        if not day_exercises:
            continue
        
        # Calculate event time (start from today + day)
        event_date = datetime.utcnow() + timedelta(days=day - 1)
        start_time = event_date.replace(hour=9, minute=0, second=0, microsecond=0)
        
        # Calculate total duration
        total_duration = sum(e.duration_minutes for e in day_exercises)
        end_time = start_time + timedelta(minutes=total_duration)
        
        # Create event description
        description = f"Day {day} Workout\n\n"
        for ex in day_exercises:
            description += f"• {ex.name}"
            if ex.sets and ex.reps:
                description += f" - {ex.sets} sets x {ex.reps} reps"
            description += "\n"
        
        # Create Google Calendar event
        google_event_id = google_calendar_service.create_event(
            token=current_user.google_calendar_token,
            title=f"{plan.title} - Day {day}",
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        
        if google_event_id:
            # Save to database
            calendar_event = CalendarEvent(
                user_id=current_user.id,
                google_event_id=google_event_id,
                title=f"{plan.title} - Day {day}",
                description=description,
                event_type="workout",
                start_time=start_time,
                end_time=end_time,
                workout_plan_id=plan.id,
                is_synced=True
            )
            db.add(calendar_event)
            synced_count += 1
    
    db.commit()
    
    return {
        "message": f"Successfully synced {synced_count} workout days to Google Calendar",
        "synced_count": synced_count
    }

@router.get("/events", response_model=List[CalendarEventResponse])
async def get_calendar_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all calendar events
    """
    events = db.query(CalendarEvent).filter(
        CalendarEvent.user_id == current_user.id
    ).order_by(CalendarEvent.start_time).all()
    
    return events

@router.delete("/disconnect")
async def disconnect_google_calendar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Disconnect Google Calendar
    """
    current_user.google_calendar_token = None
    current_user.google_refresh_token = None
    
    db.commit()
    
    return {"message": "Google Calendar disconnected successfully"}

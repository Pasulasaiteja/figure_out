"""
Progress Tracking Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.progress import ProgressRecord
from app.schemas.progress import ProgressRecordCreate, ProgressRecordResponse, ProgressSummary
from datetime import datetime, timedelta
from typing import List
import random

router = APIRouter()

@router.post("/seed")
async def seed_sample_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate sample progress data for the last 30 days
    """
    # Check if user already has data
    existing = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id
    ).first()
    
    if existing:
        # Delete existing data to reseed
        db.query(ProgressRecord).filter(
            ProgressRecord.user_id == current_user.id
        ).delete()
        db.commit()
    
    # Generate 30 days of sample data
    base_weight = current_user.weight or 70.0
    records_created = []
    
    for i in range(30, 0, -1):
        date = datetime.utcnow() - timedelta(days=i)
        
        # Simulate realistic progress
        weight_change = random.uniform(-0.1, 0.05) * (30 - i) / 30  # Gradual weight loss
        workout_done = random.choice([0, 1, 1, 1])  # 75% chance of workout
        
        record = ProgressRecord(
            user_id=current_user.id,
            record_date=date,
            weight=round(base_weight + weight_change, 1),
            body_fat_percentage=round(random.uniform(15, 25), 1) if random.random() > 0.5 else None,
            workout_completed=workout_done,
            calories_burned=random.randint(200, 500) if workout_done else random.randint(50, 150),
            workout_duration=random.randint(30, 60) if workout_done else 0,
            calories_consumed=random.randint(1800, 2500),
            protein_consumed=round(random.uniform(80, 150), 1),
            water_intake=round(random.uniform(1.5, 3.5), 1),
            sleep_hours=round(random.uniform(5, 9), 1),
            energy_level=random.choice(["Low", "Medium", "High"]),
            mood=random.choice(["Good", "Neutral", "Bad"]),
            notes=random.choice([
                "Great workout today!",
                "Felt tired but pushed through",
                "Rest day, focused on recovery",
                "New personal best!",
                None
            ])
        )
        db.add(record)
        records_created.append(record)
    
    # Update user streak
    current_user.workout_streak = random.randint(5, 15)
    current_user.total_calories_burned = sum(r.calories_burned for r in records_created)
    
    db.commit()
    
    return {"message": f"Created {len(records_created)} sample progress records", "count": len(records_created)}

@router.post("/", response_model=ProgressRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_progress_record(
    record_data: ProgressRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new progress record
    """
    new_record = ProgressRecord(
        user_id=current_user.id,
        **record_data.dict()
    )
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    
    return new_record

@router.get("/", response_model=List[ProgressRecordResponse])
async def get_progress_records(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get progress records for the last N days
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    records = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.record_date >= start_date
    ).order_by(ProgressRecord.record_date.desc()).all()
    
    return records

@router.get("/summary", response_model=ProgressSummary)
async def get_progress_summary(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get progress summary with analytics
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    records = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.record_date >= start_date
    ).order_by(ProgressRecord.record_date).all()
    
    if not records:
        return {
            "total_workouts": 0,
            "total_calories_burned": 0,
            "current_streak": current_user.workout_streak,
            "weight_change": None,
            "average_workout_duration": 0,
            "records": []
        }
    
    # Calculate stats
    total_workouts = sum(r.workout_completed for r in records)
    total_calories = sum(r.calories_burned for r in records)
    
    # Weight change
    weight_records = [r for r in records if r.weight is not None]
    weight_change = None
    if len(weight_records) >= 2:
        weight_change = weight_records[-1].weight - weight_records[0].weight
    
    # Average workout duration
    workout_durations = [r.workout_duration for r in records if r.workout_duration > 0]
    avg_duration = sum(workout_durations) / len(workout_durations) if workout_durations else 0
    
    return {
        "total_workouts": total_workouts,
        "total_calories_burned": total_calories,
        "current_streak": current_user.workout_streak,
        "weight_change": round(weight_change, 1) if weight_change else None,
        "average_workout_duration": round(avg_duration, 1),
        "records": records
    }

@router.get("/charts")
async def get_chart_data(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get data formatted for charts
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    records = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.record_date >= start_date
    ).order_by(ProgressRecord.record_date).all()
    
    # Format data for charts
    calories_data = [
        {
            "date": r.record_date.strftime("%Y-%m-%d"),
            "calories": r.calories_burned
        }
        for r in records
    ]
    
    weight_data = [
        {
            "date": r.record_date.strftime("%Y-%m-%d"),
            "weight": r.weight
        }
        for r in records if r.weight is not None
    ]
    
    workout_data = [
        {
            "date": r.record_date.strftime("%Y-%m-%d"),
            "workouts": r.workout_completed
        }
        for r in records
    ]
    
    return {
        "calories": calories_data,
        "weight": weight_data,
        "workouts": workout_data
    }

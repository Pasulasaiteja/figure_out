"""
Workout Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.workout import WorkoutPlan, Exercise
from app.models.health_assessment import HealthAssessment
from app.schemas.workout import WorkoutPlanResponse, ExerciseResponse, ExerciseComplete
from app.services.ai_service import ai_service
from app.services.youtube_service import youtube_service
from datetime import datetime

router = APIRouter()

@router.post("/generate", response_model=WorkoutPlanResponse)
async def generate_workout_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered 7-day workout plan
    """
    # Get user's health assessment
    assessment = db.query(HealthAssessment).filter(
        HealthAssessment.user_id == current_user.id
    ).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete health assessment first"
        )
    
    # Deactivate old plans
    db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id
    ).update({"is_active": False})
    
    # Prepare data for AI
    user_data = {
        "name": current_user.name,
        "age": current_user.age,
        "weight": current_user.weight,
        "height": current_user.height
    }
    
    assessment_data = {
        "fitness_level": assessment.fitness_level,
        "fitness_goals": assessment.fitness_goals,
        "workout_preference": assessment.workout_preference,
        "time_availability": assessment.time_availability,
        "injuries": assessment.injuries
    }
    
    # Generate plan using AI
    ai_plan = ai_service.generate_workout_plan(user_data, assessment_data)
    
    # Create workout plan
    new_plan = WorkoutPlan(
        user_id=current_user.id,
        title=ai_plan.get("title", "Your Custom Workout Plan"),
        description=ai_plan.get("description", ""),
        duration_days=7,
        difficulty_level=ai_plan.get("difficulty_level", assessment.fitness_level),
        is_active=True
    )
    
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    # Add exercises
    for exercise_data in ai_plan.get("exercises", []):
        # Use provided YouTube video ID if available, otherwise search
        video_id = exercise_data.get("youtube_video_id")
        if not video_id:
            video_id = youtube_service.search_exercise_video(exercise_data.get("name", ""))
        
        exercise = Exercise(
            workout_plan_id=new_plan.id,
            day=exercise_data.get("day", 1),
            name=exercise_data.get("name", ""),
            description=exercise_data.get("description", ""),
            category=exercise_data.get("category", "Strength"),
            sets=exercise_data.get("sets"),
            reps=exercise_data.get("reps"),
            rest_period=exercise_data.get("rest_period"),
            youtube_video_id=video_id,
            instructions=exercise_data.get("instructions", ""),
            estimated_calories=exercise_data.get("estimated_calories", 0),
            duration_minutes=exercise_data.get("duration_minutes", 0),
            fitness_tip=exercise_data.get("fitness_tip")
        )
        db.add(exercise)
    
    db.commit()
    db.refresh(new_plan)
    
    return new_plan

@router.get("/current", response_model=WorkoutPlanResponse)
async def get_current_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current active workout plan
    """
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.is_active == True
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active workout plan found. Generate one first."
        )
    
    return plan

@router.get("/day/{day}", response_model=list[ExerciseResponse])
async def get_day_exercises(
    day: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get exercises for a specific day
    """
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.is_active == True
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active workout plan found"
        )
    
    exercises = db.query(Exercise).filter(
        Exercise.workout_plan_id == plan.id,
        Exercise.day == day
    ).all()
    
    return exercises

@router.post("/complete", response_model=ExerciseResponse)
async def complete_exercise(
    completion_data: ExerciseComplete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark exercise as completed and update stats
    """
    exercise = db.query(Exercise).filter(
        Exercise.id == completion_data.exercise_id
    ).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )
    
    # Mark as completed
    exercise.is_completed = True
    exercise.completed_at = datetime.utcnow()
    
    # Update user stats
    calories = completion_data.calories_burned or exercise.estimated_calories
    current_user.total_calories_burned += calories
    
    # Update charity contribution (1 calorie = 1 rupee)
    current_user.charity_contribution += calories
    
    db.commit()
    db.refresh(exercise)
    
    return exercise

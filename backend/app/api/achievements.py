"""
Achievements and Gamification Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.achievement import Achievement, UserAchievement
from app.schemas.achievement import AchievementResponse, UserAchievementResponse
from typing import List

router = APIRouter()

def check_and_award_achievements(user: User, db: Session):
    """
    Check user stats and award new achievements
    """
    # Get all achievements
    all_achievements = db.query(Achievement).all()
    
    # Get user's current achievements
    user_achievement_ids = [
        ua.achievement_id 
        for ua in db.query(UserAchievement).filter(
            UserAchievement.user_id == user.id
        ).all()
    ]
    
    newly_awarded = []
    
    for achievement in all_achievements:
        # Skip if already awarded
        if achievement.id in user_achievement_ids:
            continue
        
        # Check criteria
        should_award = False
        
        if achievement.criteria_type == "streak":
            if user.workout_streak >= achievement.criteria_value:
                should_award = True
        
        elif achievement.criteria_type == "calories":
            if user.total_calories_burned >= achievement.criteria_value:
                should_award = True
        
        elif achievement.criteria_type == "workouts":
            # Count total completed workouts
            from app.models.workout import Exercise
            completed_workouts = db.query(Exercise).filter(
                Exercise.is_completed == True
            ).count()
            if completed_workouts >= achievement.criteria_value:
                should_award = True
        
        # Award achievement
        if should_award:
            user_achievement = UserAchievement(
                user_id=user.id,
                achievement_id=achievement.id
            )
            db.add(user_achievement)
            newly_awarded.append(achievement)
    
    if newly_awarded:
        db.commit()
    
    return newly_awarded

@router.get("/", response_model=List[AchievementResponse])
async def get_all_achievements(db: Session = Depends(get_db)):
    """
    Get all available achievements
    """
    achievements = db.query(Achievement).all()
    return achievements

@router.get("/my", response_model=List[UserAchievementResponse])
async def get_my_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's unlocked achievements
    """
    user_achievements = db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.id
    ).all()
    
    return user_achievements

@router.get("/check")
async def check_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check and award new achievements
    """
    newly_awarded = check_and_award_achievements(current_user, db)
    
    return {
        "message": f"Checked achievements. {len(newly_awarded)} new achievements unlocked.",
        "new_achievements": [
            {
                "name": a.name,
                "description": a.description,
                "badge_icon": a.badge_icon
            }
            for a in newly_awarded
        ]
    }

@router.post("/mark-viewed/{achievement_id}")
async def mark_achievement_viewed(
    achievement_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark achievement as viewed
    """
    user_achievement = db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.id,
        UserAchievement.achievement_id == achievement_id
    ).first()
    
    if not user_achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found"
        )
    
    user_achievement.is_viewed = True
    db.commit()
    
    return {"message": "Achievement marked as viewed"}

@router.post("/seed")
async def seed_achievements(db: Session = Depends(get_db)):
    """
    Seed default achievements (run once)
    """
    default_achievements = [
        {
            "name": "First Step",
            "description": "Complete your first workout",
            "badge_icon": "🏃",
            "badge_color": "#4CAF50",
            "criteria_type": "workouts",
            "criteria_value": 1
        },
        {
            "name": "Week Warrior",
            "description": "Maintain a 7-day workout streak",
            "badge_icon": "🔥",
            "badge_color": "#FF5722",
            "criteria_type": "streak",
            "criteria_value": 7
        },
        {
            "name": "Calorie Crusher",
            "description": "Burn 1000 total calories",
            "badge_icon": "💪",
            "badge_color": "#FF9800",
            "criteria_type": "calories",
            "criteria_value": 1000
        },
        {
            "name": "Consistency King",
            "description": "Complete 30 workouts",
            "badge_icon": "👑",
            "badge_color": "#FFD700",
            "criteria_type": "workouts",
            "criteria_value": 30
        },
        {
            "name": "Century Club",
            "description": "Complete 100 workouts",
            "badge_icon": "🏆",
            "badge_color": "#9C27B0",
            "criteria_type": "workouts",
            "criteria_value": 100
        }
    ]
    
    for ach_data in default_achievements:
        # Check if already exists
        existing = db.query(Achievement).filter(
            Achievement.name == ach_data["name"]
        ).first()
        
        if not existing:
            achievement = Achievement(**ach_data)
            db.add(achievement)
    
    db.commit()
    
    return {"message": "Achievements seeded successfully"}

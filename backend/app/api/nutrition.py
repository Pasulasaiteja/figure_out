"""
Nutrition Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.nutrition import NutritionPlan, Meal
from app.models.health_assessment import HealthAssessment
from app.schemas.nutrition import NutritionPlanResponse, MealResponse, GroceryListResponse
from app.services.ai_service import ai_service
from typing import List

router = APIRouter()

@router.post("/generate", response_model=NutritionPlanResponse)
async def generate_nutrition_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered 7-day nutrition plan
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
    db.query(NutritionPlan).filter(
        NutritionPlan.user_id == current_user.id
    ).update({"is_active": False})
    
    # Prepare data for AI
    user_data = {
        "name": current_user.name,
        "age": current_user.age,
        "weight": current_user.weight,
        "height": current_user.height
    }
    
    assessment_data = {
        "calorie_target": assessment.calorie_target,
        "diet_type": assessment.diet_type,
        "dietary_restrictions": assessment.dietary_restrictions,
        "allergies": assessment.allergies,
        "fitness_goals": assessment.fitness_goals
    }
    
    # Generate plan using AI
    ai_plan = ai_service.generate_nutrition_plan(user_data, assessment_data)
    
    # Create nutrition plan
    new_plan = NutritionPlan(
        user_id=current_user.id,
        title=ai_plan.get("title", "Your Custom Nutrition Plan"),
        description=ai_plan.get("description", ""),
        duration_days=7,
        daily_calorie_target=ai_plan.get("daily_calorie_target", assessment.calorie_target),
        is_active=True
    )
    
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    # Add meals
    for meal_data in ai_plan.get("meals", []):
        meal = Meal(
            nutrition_plan_id=new_plan.id,
            day=meal_data.get("day", 1),
            meal_type=meal_data.get("meal_type", "Breakfast"),
            name=meal_data.get("name", ""),
            description=meal_data.get("description", ""),
            calories=meal_data.get("calories", 0),
            protein=meal_data.get("protein", 0),
            carbs=meal_data.get("carbs", 0),
            fat=meal_data.get("fat", 0),
            fiber=meal_data.get("fiber", 0),
            ingredients=meal_data.get("ingredients", []),
            recipe_instructions=meal_data.get("recipe_instructions", ""),
            prep_time=meal_data.get("prep_time", 0),
            cook_time=meal_data.get("cook_time", 0)
        )
        db.add(meal)
    
    db.commit()
    db.refresh(new_plan)
    
    return new_plan

@router.get("/current", response_model=NutritionPlanResponse)
async def get_current_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current active nutrition plan
    """
    plan = db.query(NutritionPlan).filter(
        NutritionPlan.user_id == current_user.id,
        NutritionPlan.is_active == True
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active nutrition plan found. Generate one first."
        )
    
    return plan

@router.get("/day/{day}", response_model=List[MealResponse])
async def get_day_meals(
    day: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get meals for a specific day
    """
    plan = db.query(NutritionPlan).filter(
        NutritionPlan.user_id == current_user.id,
        NutritionPlan.is_active == True
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active nutrition plan found"
        )
    
    meals = db.query(Meal).filter(
        Meal.nutrition_plan_id == plan.id,
        Meal.day == day
    ).all()
    
    return meals

@router.get("/grocery-list", response_model=GroceryListResponse)
async def get_grocery_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate grocery list from current nutrition plan
    """
    plan = db.query(NutritionPlan).filter(
        NutritionPlan.user_id == current_user.id,
        NutritionPlan.is_active == True
    ).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active nutrition plan found"
        )
    
    # Collect all ingredients
    all_ingredients = set()
    for meal in plan.meals:
        if meal.ingredients:
            for ingredient in meal.ingredients:
                all_ingredients.add(ingredient)
    
    # Generate BigBasket URL
    bigbasket_url = "https://www.bigbasket.com/"
    
    return {
        "ingredients": sorted(list(all_ingredients)),
        "bigbasket_url": bigbasket_url
    }

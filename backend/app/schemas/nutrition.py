"""
Nutrition Schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MealBase(BaseModel):
    day: int
    meal_type: str  # Breakfast, Lunch, Dinner, Snack
    name: str
    description: Optional[str] = None
    calories: int
    protein: float
    carbs: float
    fat: float
    fiber: float = 0
    ingredients: Optional[List[str]] = []
    recipe_instructions: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    recipe_url: Optional[str] = None
    image_url: Optional[str] = None

class MealCreate(MealBase):
    pass

class MealResponse(MealBase):
    id: int
    nutrition_plan_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class NutritionPlanBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_days: int = 7
    daily_calorie_target: int

class NutritionPlanCreate(NutritionPlanBase):
    meals: List[MealCreate]

class NutritionPlanResponse(NutritionPlanBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    meals: List[MealResponse] = []
    
    class Config:
        from_attributes = True

class GroceryListResponse(BaseModel):
    ingredients: List[str]
    bigbasket_url: str

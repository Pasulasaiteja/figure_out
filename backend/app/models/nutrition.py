"""
Nutrition Plan and Meal Models
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class NutritionPlan(Base):
    __tablename__ = "nutrition_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    title = Column(String, nullable=False)
    description = Column(Text)
    duration_days = Column(Integer, default=7)
    daily_calorie_target = Column(Integer)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="nutrition_plans")
    meals = relationship("Meal", back_populates="nutrition_plan", cascade="all, delete-orphan")

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    nutrition_plan_id = Column(Integer, ForeignKey("nutrition_plans.id"))
    
    day = Column(Integer)  # 1-7
    meal_type = Column(String)  # Breakfast, Lunch, Dinner, Snack
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Nutritional Information
    calories = Column(Integer)
    protein = Column(Float)  # grams
    carbs = Column(Float)  # grams
    fat = Column(Float)  # grams
    fiber = Column(Float, default=0)  # grams
    
    # Recipe Information
    ingredients = Column(JSON)  # List of ingredients
    recipe_instructions = Column(Text)
    prep_time = Column(Integer)  # minutes
    cook_time = Column(Integer)  # minutes
    
    # External Integration
    spoonacular_id = Column(Integer, nullable=True)
    recipe_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    nutrition_plan = relationship("NutritionPlan", back_populates="meals")

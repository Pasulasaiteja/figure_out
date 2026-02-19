"""
Spoonacular API Service for Nutrition and Recipes
"""
import requests
from app.core.config import settings
from typing import List, Dict, Optional

class SpoonacularService:
    def __init__(self):
        self.api_key = settings.SPOONACULAR_API_KEY
        self.base_url = "https://api.spoonacular.com"
    
    def search_recipes(self, query: str, diet: str = None, max_results: int = 5) -> List[Dict]:
        """
        Search for recipes based on query and diet type
        """
        if not self.api_key:
            return []
        
        try:
            params = {
                "query": query,
                "number": max_results,
                "apiKey": self.api_key
            }
            
            if diet and diet.lower() != "none":
                params["diet"] = diet.lower()
            
            response = requests.get(f"{self.base_url}/recipes/complexSearch", params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            print(f"Spoonacular API Error: {e}")
            return []
    
    def get_recipe_details(self, recipe_id: int) -> Optional[Dict]:
        """
        Get detailed recipe information including ingredients and instructions
        """
        if not self.api_key:
            return None
        
        try:
            params = {
                "apiKey": self.api_key,
                "includeNutrition": True
            }
            
            response = requests.get(
                f"{self.base_url}/recipes/{recipe_id}/information",
                params=params
            )
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Spoonacular API Error: {e}")
            return None
    
    def get_meal_nutrition(self, recipe_id: int) -> Optional[Dict]:
        """
        Get nutritional breakdown of a recipe
        """
        recipe_details = self.get_recipe_details(recipe_id)
        
        if not recipe_details:
            return None
        
        nutrition = recipe_details.get("nutrition", {})
        nutrients = nutrition.get("nutrients", [])
        
        # Extract key nutrients
        nutrition_data = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0
        }
        
        for nutrient in nutrients:
            name = nutrient.get("name", "").lower()
            amount = nutrient.get("amount", 0)
            
            if "calories" in name:
                nutrition_data["calories"] = int(amount)
            elif "protein" in name:
                nutrition_data["protein"] = round(amount, 1)
            elif "carbohydrate" in name:
                nutrition_data["carbs"] = round(amount, 1)
            elif "fat" in name and "saturated" not in name:
                nutrition_data["fat"] = round(amount, 1)
            elif "fiber" in name:
                nutrition_data["fiber"] = round(amount, 1)
        
        return nutrition_data
    
    def generate_grocery_list(self, recipe_ids: List[int]) -> List[str]:
        """
        Generate grocery list from multiple recipes
        """
        if not self.api_key or not recipe_ids:
            return []
        
        try:
            ingredients = set()
            
            for recipe_id in recipe_ids:
                details = self.get_recipe_details(recipe_id)
                if details and "extendedIngredients" in details:
                    for ingredient in details["extendedIngredients"]:
                        ingredients.add(ingredient["original"])
            
            return sorted(list(ingredients))
        except Exception as e:
            print(f"Spoonacular API Error: {e}")
            return []

# Singleton instance
spoonacular_service = SpoonacularService()

"""
Groq AI Service for Workout and Nutrition Plan Generation
"""
from groq import Groq
from app.core.config import settings
import json
from typing import Dict, List

class AIService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
    
    def generate_workout_plan(self, user_data: Dict, assessment_data: Dict) -> Dict:
        """
        Generate personalized 7-day workout plan using AI
        """
        prompt = f"""
You are an expert fitness coach. Generate a detailed 7-day workout plan in JSON format.

User Profile:
- Fitness Level: {assessment_data.get('fitness_level')}
- Goals: {assessment_data.get('fitness_goals')}
- Workout Preference: {assessment_data.get('workout_preference')}
- Time Available: {assessment_data.get('time_availability')}
- Injuries/Limitations: {assessment_data.get('injuries', 'None')}

Requirements:
1. Create 5-7 exercises per day
2. Include warmup, main exercises, and cooldown
3. Provide sets, reps, rest periods
4. Add a daily fitness tip
5. Estimate calories burned per exercise
6. Return ONLY valid JSON, no additional text

JSON Format:
{{
  "title": "plan title",
  "description": "plan description",
  "difficulty_level": "Beginner|Intermediate|Advanced",
  "exercises": [
    {{
      "day": 1,
      "name": "Exercise Name",
      "description": "Brief description",
      "category": "Warmup|Strength|Cardio|Cooldown",
      "sets": 3,
      "reps": "12",
      "rest_period": "60 seconds",
      "instructions": "Step by step instructions",
      "estimated_calories": 50,
      "duration_minutes": 10,
      "fitness_tip": "Daily motivation tip"
    }}
  ]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            plan = json.loads(content)
            return plan
        except Exception as e:
            print(f"AI Generation Error: {e}")
            return self._get_default_workout_plan(assessment_data)
    
    def generate_nutrition_plan(self, user_data: Dict, assessment_data: Dict) -> Dict:
        """
        Generate personalized 7-day nutrition plan using AI
        """
        prompt = f"""
You are an expert nutritionist. Generate a detailed 7-day meal plan in JSON format.

User Profile:
- Calorie Target: {assessment_data.get('calorie_target')} calories/day
- Diet Type: {assessment_data.get('diet_type')}
- Dietary Restrictions: {assessment_data.get('dietary_restrictions', 'None')}
- Allergies: {assessment_data.get('allergies', 'None')}
- Fitness Goals: {assessment_data.get('fitness_goals')}

Requirements:
1. Create Breakfast, Lunch, Dinner for 7 days
2. Provide macro breakdown (protein, carbs, fat)
3. Include ingredients and recipe instructions
4. Stay within daily calorie target
5. Return ONLY valid JSON, no additional text

JSON Format:
{{
  "title": "plan title",
  "description": "plan description",
  "daily_calorie_target": 2000,
  "meals": [
    {{
      "day": 1,
      "meal_type": "Breakfast|Lunch|Dinner",
      "name": "Meal Name",
      "description": "Brief description",
      "calories": 500,
      "protein": 25.0,
      "carbs": 50.0,
      "fat": 15.0,
      "fiber": 8.0,
      "ingredients": ["ingredient 1", "ingredient 2"],
      "recipe_instructions": "Step by step cooking instructions",
      "prep_time": 10,
      "cook_time": 20
    }}
  ]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            plan = json.loads(content)
            return plan
        except Exception as e:
            print(f"AI Generation Error: {e}")
            return self._get_default_nutrition_plan(assessment_data)
    
    def chat_with_aromi(self, message: str, user_context: Dict, chat_history: List[Dict]) -> str:
        """
        AROMI AI Coach - Conversational health coaching
        """
        system_prompt = f"""
You are AROMI, an empathetic and knowledgeable AI fitness and wellness coach. 
You help users with workout adjustments, nutrition advice, motivation, and health guidance.

User Context:
- Fitness Level: {user_context.get('fitness_level', 'Unknown')}
- Goals: {user_context.get('fitness_goals', 'General fitness')}
- Current Streak: {user_context.get('workout_streak', 0)} days
- Calories Burned Today: {user_context.get('calories_burned_today', 0)}

Capabilities:
- Adjust workout plans (if injured, traveling, busy, low energy)
- Suggest alternative exercises
- Provide meal suggestions and nutrition tips
- Give hydration reminders
- Offer motivation and support
- Track progress and celebrate achievements

Be conversational, supportive, and actionable. Keep responses concise (2-4 sentences).
"""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history (last 10 messages for context)
        for msg in chat_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AROMI Chat Error: {e}")
            return "I'm having trouble connecting right now. Please try again in a moment."
    
    def _get_default_workout_plan(self, assessment: Dict) -> Dict:
        """Fallback workout plan if AI fails - Complete 7-day plan with YouTube videos"""
        fitness_level = assessment.get('fitness_level', 'Beginner')
        
        return {
            "title": f"7-Day {fitness_level} Transformation Plan",
            "description": "A complete workout program designed to build strength, improve endurance, and boost your fitness",
            "difficulty_level": fitness_level,
            "exercises": [
                # Day 1 - Upper Body
                {"day": 1, "name": "Arm Circles Warmup", "description": "Shoulder mobility warmup", "category": "Warmup", "sets": 2, "reps": "30 seconds", "rest_period": "15 seconds", "instructions": "Extend arms out and make small circles, gradually increasing size", "estimated_calories": 15, "duration_minutes": 2, "fitness_tip": "Always warm up to prevent injury!", "youtube_video_id": "140RTNMciH8"},
                {"day": 1, "name": "Push-Ups", "description": "Classic chest and triceps builder", "category": "Strength", "sets": 3, "reps": "10-15", "rest_period": "60 seconds", "instructions": "Keep body straight, lower chest to ground, push back up", "estimated_calories": 50, "duration_minutes": 5, "fitness_tip": "Keep your core engaged throughout!", "youtube_video_id": "IODxDxX7oi4"},
                {"day": 1, "name": "Dumbbell Rows", "description": "Build back strength", "category": "Strength", "sets": 3, "reps": "12", "rest_period": "60 seconds", "instructions": "Hinge at hips, pull weight to hip, squeeze shoulder blade", "estimated_calories": 45, "duration_minutes": 6, "fitness_tip": "Focus on squeezing your back muscles", "youtube_video_id": "pYcpY20QaE8"},
                {"day": 1, "name": "Shoulder Press", "description": "Build shoulder strength", "category": "Strength", "sets": 3, "reps": "10", "rest_period": "60 seconds", "instructions": "Press weights overhead, fully extend arms", "estimated_calories": 40, "duration_minutes": 5, "fitness_tip": "Don't arch your back excessively", "youtube_video_id": "qEwKCR5JCog"},
                {"day": 1, "name": "Tricep Dips", "description": "Target triceps effectively", "category": "Strength", "sets": 3, "reps": "12", "rest_period": "45 seconds", "instructions": "Lower body by bending elbows, push back up", "estimated_calories": 35, "duration_minutes": 4, "fitness_tip": "Keep elbows pointing backward", "youtube_video_id": "0326dy_-CzM"},
                {"day": 1, "name": "Arm Stretches", "description": "Cool down stretches", "category": "Cooldown", "sets": 1, "reps": "60 seconds", "rest_period": "0", "instructions": "Stretch triceps, biceps, and shoulders gently", "estimated_calories": 10, "duration_minutes": 3, "fitness_tip": "Stretching improves recovery!", "youtube_video_id": "Qy3U5Q5mF6E"},
                
                # Day 2 - Lower Body
                {"day": 2, "name": "Leg Swings", "description": "Dynamic leg warmup", "category": "Warmup", "sets": 2, "reps": "15 each leg", "rest_period": "15 seconds", "instructions": "Swing leg forward and back, then side to side", "estimated_calories": 20, "duration_minutes": 3, "fitness_tip": "Start your workout with dynamic stretches!", "youtube_video_id": "gC4j-lnra_M"},
                {"day": 2, "name": "Squats", "description": "King of leg exercises", "category": "Strength", "sets": 4, "reps": "15", "rest_period": "60 seconds", "instructions": "Lower hips back and down, keep chest up, drive through heels", "estimated_calories": 70, "duration_minutes": 7, "fitness_tip": "Depth matters - aim for parallel or below!", "youtube_video_id": "aclHkVaku9U"},
                {"day": 2, "name": "Lunges", "description": "Unilateral leg strength", "category": "Strength", "sets": 3, "reps": "12 each leg", "rest_period": "45 seconds", "instructions": "Step forward, lower back knee toward ground, push back", "estimated_calories": 60, "duration_minutes": 6, "fitness_tip": "Keep your front knee over your ankle", "youtube_video_id": "QOVaHwm-Q6U"},
                {"day": 2, "name": "Glute Bridges", "description": "Activate and strengthen glutes", "category": "Strength", "sets": 3, "reps": "15", "rest_period": "45 seconds", "instructions": "Lie on back, drive hips up, squeeze glutes at top", "estimated_calories": 40, "duration_minutes": 5, "fitness_tip": "Squeeze hard at the top!", "youtube_video_id": "OUgsJ8-Vi0E"},
                {"day": 2, "name": "Calf Raises", "description": "Build strong calves", "category": "Strength", "sets": 3, "reps": "20", "rest_period": "30 seconds", "instructions": "Rise up on toes, hold briefly, lower slowly", "estimated_calories": 25, "duration_minutes": 4, "fitness_tip": "Go slow on the way down", "youtube_video_id": "gwLzBJYoWlI"},
                {"day": 2, "name": "Quad Stretch", "description": "Cool down leg stretches", "category": "Cooldown", "sets": 1, "reps": "45 seconds each", "rest_period": "0", "instructions": "Pull heel to glute, hold, switch legs", "estimated_calories": 10, "duration_minutes": 3, "fitness_tip": "Never skip your cool down!", "youtube_video_id": "WnqWOAGWlpc"},
                
                # Day 3 - Cardio & Core
                {"day": 3, "name": "Jumping Jacks", "description": "Get your heart pumping", "category": "Warmup", "sets": 3, "reps": "30 seconds", "rest_period": "15 seconds", "instructions": "Jump feet out while raising arms, jump back together", "estimated_calories": 35, "duration_minutes": 3, "fitness_tip": "Great for elevating heart rate!", "youtube_video_id": "c4DAnQ6DtF8"},
                {"day": 3, "name": "High Knees", "description": "Cardio and core engagement", "category": "Cardio", "sets": 3, "reps": "30 seconds", "rest_period": "30 seconds", "instructions": "Run in place bringing knees high toward chest", "estimated_calories": 50, "duration_minutes": 4, "fitness_tip": "Pump your arms for more intensity!", "youtube_video_id": "oDdkytliOqE"},
                {"day": 3, "name": "Mountain Climbers", "description": "Full body cardio blast", "category": "Cardio", "sets": 3, "reps": "30 seconds", "rest_period": "30 seconds", "instructions": "In plank position, drive knees to chest alternating", "estimated_calories": 55, "duration_minutes": 4, "fitness_tip": "Keep hips level throughout!", "youtube_video_id": "nmwgirgXLYM"},
                {"day": 3, "name": "Plank Hold", "description": "Core stability builder", "category": "Strength", "sets": 3, "reps": "30-45 seconds", "rest_period": "45 seconds", "instructions": "Hold body straight in forearm position", "estimated_calories": 25, "duration_minutes": 4, "fitness_tip": "Breathe steadily, don't hold breath!", "youtube_video_id": "ASdvN_XEl_c"},
                {"day": 3, "name": "Bicycle Crunches", "description": "Target obliques effectively", "category": "Strength", "sets": 3, "reps": "20 each side", "rest_period": "30 seconds", "instructions": "Rotate torso bringing elbow to opposite knee", "estimated_calories": 40, "duration_minutes": 5, "fitness_tip": "Quality over speed!", "youtube_video_id": "9FGilxCbdz8"},
                {"day": 3, "name": "Child's Pose", "description": "Relaxing cool down", "category": "Cooldown", "sets": 1, "reps": "60 seconds", "rest_period": "0", "instructions": "Kneel, sit back on heels, stretch arms forward", "estimated_calories": 5, "duration_minutes": 2, "fitness_tip": "Focus on deep breathing!", "youtube_video_id": "2MJGg-dUKh0"},
                
                # Day 4 - Active Recovery / Flexibility
                {"day": 4, "name": "Cat-Cow Stretch", "description": "Spine mobility", "category": "Warmup", "sets": 2, "reps": "10", "rest_period": "15 seconds", "instructions": "On hands and knees, arch and round back alternating", "estimated_calories": 15, "duration_minutes": 3, "fitness_tip": "Move slowly and mindfully!", "youtube_video_id": "kqnua4rHVVA"},
                {"day": 4, "name": "Standing Forward Fold", "description": "Hamstring stretch", "category": "Warmup", "sets": 2, "reps": "30 seconds", "rest_period": "15 seconds", "instructions": "Bend forward from hips, let head hang", "estimated_calories": 10, "duration_minutes": 2, "fitness_tip": "Bend knees if needed!", "youtube_video_id": "g7Uhp5tphAs"},
                {"day": 4, "name": "Hip Flexor Stretch", "description": "Open tight hips", "category": "Strength", "sets": 2, "reps": "30 seconds each", "rest_period": "15 seconds", "instructions": "Lunge position, drive hips forward gently", "estimated_calories": 15, "duration_minutes": 3, "fitness_tip": "Tight hips can cause lower back pain!", "youtube_video_id": "YQmpO9VT2X4"},
                {"day": 4, "name": "Yoga Flow", "description": "Sun salutation sequence", "category": "Cardio", "sets": 3, "reps": "5 flows", "rest_period": "30 seconds", "instructions": "Flow through downward dog, plank, cobra, downward dog", "estimated_calories": 45, "duration_minutes": 10, "fitness_tip": "Yoga improves flexibility and reduces stress!", "youtube_video_id": "sTANio_2E0Q"},
                {"day": 4, "name": "Pigeon Pose", "description": "Deep hip opener", "category": "Cooldown", "sets": 1, "reps": "45 seconds each", "rest_period": "0", "instructions": "From downward dog, bring one knee forward, extend back leg", "estimated_calories": 10, "duration_minutes": 4, "fitness_tip": "Recovery days are crucial for muscle growth!", "youtube_video_id": "0r-0BjVazZk"},
                
                # Day 5 - Full Body Strength
                {"day": 5, "name": "Dynamic Stretches", "description": "Full body warmup", "category": "Warmup", "sets": 1, "reps": "5 minutes", "rest_period": "0", "instructions": "Arm circles, leg swings, torso twists", "estimated_calories": 25, "duration_minutes": 5, "fitness_tip": "A good warmup primes your nervous system!", "youtube_video_id": "HDfvxYuca7g"},
                {"day": 5, "name": "Burpees", "description": "Ultimate full body exercise", "category": "Cardio", "sets": 3, "reps": "10", "rest_period": "60 seconds", "instructions": "Squat down, jump feet back, push-up, jump feet in, jump up", "estimated_calories": 80, "duration_minutes": 6, "fitness_tip": "Modify by stepping instead of jumping!", "youtube_video_id": "dZgVxmf6jkA"},
                {"day": 5, "name": "Deadlifts", "description": "Posterior chain builder", "category": "Strength", "sets": 4, "reps": "10", "rest_period": "90 seconds", "instructions": "Hinge at hips, keep back straight, drive through heels", "estimated_calories": 65, "duration_minutes": 8, "fitness_tip": "Start light and focus on form!", "youtube_video_id": "op9kVnSso6Q"},
                {"day": 5, "name": "Plank to Push-up", "description": "Core and upper body combo", "category": "Strength", "sets": 3, "reps": "10", "rest_period": "45 seconds", "instructions": "Start in forearm plank, push up to hands one arm at a time", "estimated_calories": 45, "duration_minutes": 5, "fitness_tip": "Keep hips stable, minimize rocking!", "youtube_video_id": "L4oFJRDAU4Q"},
                {"day": 5, "name": "Squat Jumps", "description": "Explosive leg power", "category": "Cardio", "sets": 3, "reps": "12", "rest_period": "45 seconds", "instructions": "Squat down, explode up, land softly", "estimated_calories": 60, "duration_minutes": 5, "fitness_tip": "Land softly to protect your joints!", "youtube_video_id": "A-cFYWvaHr0"},
                {"day": 5, "name": "Full Body Stretch", "description": "Complete cool down", "category": "Cooldown", "sets": 1, "reps": "5 minutes", "rest_period": "0", "instructions": "Stretch all major muscle groups slowly", "estimated_calories": 15, "duration_minutes": 5, "fitness_tip": "Hold each stretch for 30 seconds!", "youtube_video_id": "g_tea8ZNk5A"},
                
                # Day 6 - Upper Body + Cardio
                {"day": 6, "name": "Shoulder Rolls", "description": "Upper body warmup", "category": "Warmup", "sets": 2, "reps": "20", "rest_period": "15 seconds", "instructions": "Roll shoulders forward then backward in circles", "estimated_calories": 10, "duration_minutes": 2, "fitness_tip": "Release tension from your shoulders!", "youtube_video_id": "H1Dw_cI8cMI"},
                {"day": 6, "name": "Diamond Push-ups", "description": "Triceps focused push-up", "category": "Strength", "sets": 3, "reps": "8-10", "rest_period": "60 seconds", "instructions": "Hands close together forming diamond, perform push-up", "estimated_calories": 45, "duration_minutes": 5, "fitness_tip": "Great for building arm definition!", "youtube_video_id": "J0DnG1_S92I"},
                {"day": 6, "name": "Superman Hold", "description": "Lower back strength", "category": "Strength", "sets": 3, "reps": "10", "rest_period": "45 seconds", "instructions": "Lie face down, lift arms and legs simultaneously", "estimated_calories": 30, "duration_minutes": 4, "fitness_tip": "Strengthen your back to improve posture!", "youtube_video_id": "z6PJMT2y8GQ"},
                {"day": 6, "name": "Boxing Punches", "description": "Cardio and upper body endurance", "category": "Cardio", "sets": 3, "reps": "60 seconds", "rest_period": "30 seconds", "instructions": "Throw jabs, crosses, hooks in boxing stance", "estimated_calories": 55, "duration_minutes": 5, "fitness_tip": "Stay light on your feet!", "youtube_video_id": "sExlxOmQ-OM"},
                {"day": 6, "name": "Renegade Rows", "description": "Core stability with back work", "category": "Strength", "sets": 3, "reps": "8 each arm", "rest_period": "60 seconds", "instructions": "In push-up position, row one weight up alternating", "estimated_calories": 50, "duration_minutes": 6, "fitness_tip": "Keep hips square to the ground!", "youtube_video_id": "pYcpY20QaE8"},
                {"day": 6, "name": "Standing Back Stretch", "description": "Cool down stretch", "category": "Cooldown", "sets": 1, "reps": "60 seconds", "rest_period": "0", "instructions": "Clasp hands, round back, stretch between shoulder blades", "estimated_calories": 5, "duration_minutes": 2, "fitness_tip": "Breathe deeply into the stretch!", "youtube_video_id": "Qy3U5Q5mF6E"},
                
                # Day 7 - Lower Body + Core
                {"day": 7, "name": "Hip Circles", "description": "Hip mobility warmup", "category": "Warmup", "sets": 2, "reps": "10 each direction", "rest_period": "15 seconds", "instructions": "Stand on one leg, make circles with other leg", "estimated_calories": 15, "duration_minutes": 3, "fitness_tip": "Mobility is the foundation of movement!", "youtube_video_id": "9kq4EmLnszc"},
                {"day": 7, "name": "Bulgarian Split Squats", "description": "Single leg strength", "category": "Strength", "sets": 3, "reps": "10 each leg", "rest_period": "60 seconds", "instructions": "Rear foot elevated, lower until front thigh is parallel", "estimated_calories": 55, "duration_minutes": 7, "fitness_tip": "Great for fixing muscle imbalances!", "youtube_video_id": "2C-uNgKwPLE"},
                {"day": 7, "name": "Romanian Deadlifts", "description": "Hamstring focus", "category": "Strength", "sets": 3, "reps": "12", "rest_period": "60 seconds", "instructions": "Hinge at hips with slight knee bend, feel hamstring stretch", "estimated_calories": 50, "duration_minutes": 6, "fitness_tip": "Push hips back, not down!", "youtube_video_id": "JCXUYuzwNrM"},
                {"day": 7, "name": "Wall Sit", "description": "Isometric leg endurance", "category": "Strength", "sets": 3, "reps": "30-45 seconds", "rest_period": "60 seconds", "instructions": "Back against wall, thighs parallel to floor, hold", "estimated_calories": 35, "duration_minutes": 4, "fitness_tip": "Mental strength is built through challenges!", "youtube_video_id": "y-wV4Lk6pSg"},
                {"day": 7, "name": "Dead Bug", "description": "Core stability exercise", "category": "Strength", "sets": 3, "reps": "10 each side", "rest_period": "30 seconds", "instructions": "On back, extend opposite arm and leg while keeping back flat", "estimated_calories": 30, "duration_minutes": 5, "fitness_tip": "Keep lower back pressed to floor!", "youtube_video_id": "I5xbsA71v1Y"},
                {"day": 7, "name": "Final Stretch Sequence", "description": "Complete cool down and celebrate", "category": "Cooldown", "sets": 1, "reps": "5 minutes", "rest_period": "0", "instructions": "Stretch all major muscles, reflect on your week's achievements", "estimated_calories": 15, "duration_minutes": 5, "fitness_tip": "You completed a full week - amazing work! Rest and repeat!", "youtube_video_id": "sTxC3J3gQEU"}
            ]
        }
    
    def _get_default_nutrition_plan(self, assessment: Dict) -> Dict:
        """Fallback nutrition plan if AI fails"""
        calorie_target = assessment.get('calorie_target', 2000)
        return {
            "title": "7-Day Balanced Nutrition Plan",
            "description": "A healthy and balanced meal plan",
            "daily_calorie_target": calorie_target,
            "meals": [
                {
                    "day": 1,
                    "meal_type": "Breakfast",
                    "name": "Oatmeal with Fruits",
                    "description": "Healthy breakfast with complex carbs",
                    "calories": int(calorie_target * 0.3),
                    "protein": 15.0,
                    "carbs": 50.0,
                    "fat": 10.0,
                    "fiber": 8.0,
                    "ingredients": ["1 cup oats", "1 banana", "1 tbsp honey", "1/2 cup berries"],
                    "recipe_instructions": "Cook oats with water, top with sliced banana and berries, drizzle honey",
                    "prep_time": 5,
                    "cook_time": 10
                }
            ]
        }

# Singleton instance
ai_service = AIService()

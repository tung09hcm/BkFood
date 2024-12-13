from website.models.mealmodel import MealModel
from datetime import datetime
import json
class MealController:
    def __init__(self):
        self.meal_model = MealModel()

    def insert_meal(self, user_id, meal_type, food_id, amount):
        date = datetime.now().strftime("%Y-%m-%d")
        response = self.meal_model.insert_meal(date, user_id, meal_type, food_id, amount)
        response = json.loads(response)
        return response["data"]

    def get_all_meal(self, user_id):
        response = self.meal_model.get_all_meal(user_id)
        response = json.loads(response)
        return response["data"]
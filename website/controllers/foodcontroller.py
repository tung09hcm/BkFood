from website.models.foodmodel import FoodModel
import json
class FoodController:
    def __init__(self):
        self.food_model = FoodModel()

    def get_foods(self):
        foods = self.food_model.get_all_foods()
        foods = json.loads(foods)
        # Đảm bảo "data" luôn tồn tại
        return foods["data"]


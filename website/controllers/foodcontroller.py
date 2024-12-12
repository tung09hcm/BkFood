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

    def add_food(self,name,ingredient_list,amount_list, file_path, desc, method):
        self.food_model.add_food(name,ingredient_list,amount_list, file_path, desc, method)

    def get_ingredient_by_food_id(self,id):
        ingredients = self.food_model.get_ingredient_by_food_id(id)
        ingredients = json.loads(ingredients)
        return ingredients["data"]
    
    def get_food_by_id(self,id):
        food = self.food_model.get_food_by_id(id)
        food = json.loads(food)
        return food["data"]
    
    def get_nutrition_by_food_id(self,id):
        nutrition = self.food_model.get_nutrition_by_food_id(id)
        return nutrition
    
    def vote(self, id_food, vote):
        self.food_model.vote(id_food, vote)
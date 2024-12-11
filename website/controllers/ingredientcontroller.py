from website.models.ingredientmodel import IngredientModel
import json
class IngredientController:
    def __init__(self):
        self.ingredient_model = IngredientModel()

    def get_ingredients(self):
        ingredients = self.ingredient_model.get_all_ingredients()
        ingredients = json.loads(ingredients)
        # Đảm bảo "data" luôn tồn tại
        return ingredients["data"]
    
    def get_ingredient_by_id(self, id):
        ingredient = self.ingredient_model.get_ingredient_by_id(id)
        ingredient = json.loads(ingredient)
        return ingredient["data"]

    def get_nutrition_by_ingre_id(self,id):
        nutrition = self.ingredient_model.get_nutrition_by_ingre_id(id)
        nutrition = json.loads(nutrition)
        return nutrition["data"]

    def add_ingredient(self,image,name,calcium, calories, carbohydrates, fats, fiber, iron, potassium, protein, vitaminA, vitaminC):
        print("ingredientcontroller run")
        self.ingredient_model.add_ingre(image,name,calcium, calories, carbohydrates, fats, fiber, iron, potassium, protein, vitaminA, vitaminC)


from website.models.basemodel import BaseModel

class IngredientModel(BaseModel):
    def __init__(self):
        super().__init__()

    def get_all_ingredients(self):
        response = self.get_client().table("ingredient").select("*").execute()
        return response.json()  # Trả về dữ liệu dưới dạng JSON

    def get_ingredient_by_id(self, id):
        response = self.get_client().table("ingredient").select("*").eq("id", id).execute()
        return response.json()  # Trả về dữ liệu dưới dạng JSON
    
    def get_nutrition_by_ingre_id(self, id):
        response = self.get_client().table("ingre_contains_nutrition").select("*").eq("ingre_id", id).execute()
        return response.json()  # Trả về dữ liệu dưới dạng JSON
    
    def add_ingre(self,image,name,calcium, calories, carbohydrates, fats, fiber, iron, potassium, protein, vitaminA, vitaminC):
        print("hi")
from website.models.basemodel import BaseModel

class FoodModel(BaseModel):
    def __init__(self):
        super().__init__()

    def get_all_foods(self):
        response = self.get_client().table("food").select("*").execute()
        return response.json()  # Trả về dữ liệu dưới dạng JSON

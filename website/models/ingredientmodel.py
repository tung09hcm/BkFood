from website.models.basemodel import BaseModel
from flask import session # type: ignore
import json
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
    
    def add_ingre(self, file_path,name,calcium, calories, carbohydrates, fats, fiber, iron, potassium, protein, vitaminA, vitaminC):
        print("file_path_in_ingre_model: "+ file_path)
        try:
            with open(file_path, 'rb') as f:
                response = self.get_client().storage.from_("ingredient").upload(
                    path= file_path,  # Đường dẫn ảnh trong bucket
                    file=f,
                    file_options={
                        "cache-control": "3600",
                        "upsert": "false",
                    },
                )
                full_path = response.full_path
                ingre_data = {
                    "name": name,
                    "create_user_id": session["user"]["id"],
                    "url_image": "https://zjpwitgacrwipwlwztsp.supabase.co/storage/v1/object/public/"+ full_path
                }
                # thêm vào bảng ingredient
                response = (
                    self.get_client()
                    .table("ingredient")
                    .insert(ingre_data)
                    .execute()
                )
                print("response: ")
                print(response)
                response = response.json()
                response = json.loads(response)

                data = response["data"][0]
                id = data['id']
                
                print(id)
                # lấy id từ response vừa thêm vào bảng ingredient
        except Exception as e:
            print(f"An error occurred: {e}")
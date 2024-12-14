from website.models.basemodel import BaseModel
from flask import session # type: ignore
import json
class FoodModel(BaseModel):
    def __init__(self):
        super().__init__()

    def get_all_foods(self):
        response = self.get_client().table("food").select("*").execute()
        return response.json()  # Trả về dữ liệu dưới dạng JSON

    def add_food(self,name,ingredient_list,amount_list, file_path, desc, method):
        try:
            with open(file_path, 'rb') as f:
                response = self.get_client().storage.from_("food").upload(
                    path= file_path,  # Đường dẫn ảnh trong bucket
                    file=f,
                    file_options={
                        "cache-control": "3600",
                        "upsert": "false",
                    },
                )
                full_path = response.full_path
                print("check before add food")
                response = (
                    self.get_client()
                    .table("food")
                    .insert([
                        {"create_user_id": session["user"]["id"], "name": name, "url_image": "https://zjpwitgacrwipwlwztsp.supabase.co/storage/v1/object/public/" + full_path, "description": desc, "method": method},
                    ])
                    .execute()
                )
                print("response after insert to food table")
                print(response)
                response = response.json()
                response = json.loads(response)

                data = response["data"][0]
                id = data['id']

                print("food_id: ")
                print(id)

                for i in range(len(ingredient_list)):
                    response = (
                        self.get_client()
                        .table("food_contains_ingre")
                        .insert([
                            {"food_id": id, "ingre_id": ingredient_list[i], "amount": float(int(amount_list[i]) / 100)}
                        ])
                        .execute()
                    )
                    

        except Exception as e:
            print(f"An error occurred: {e}")    
        
    def get_ingredient_by_food_id(self, id):
        # Lấy dữ liệu từ bảng food_contains_ingre với food_id tương ứng
        response = self.get_client().table("food_contains_ingre").select("*, ingredient(name, url_image, id, ingre_contains_nutrition(*))").eq("food_id", id).execute()
        tra_ve = response.json()
        print(tra_ve)
        return tra_ve
        
    def get_food_by_id(self,id):
        response = self.get_client().table("food").select("*").eq("id", id).execute()
        return response.json()
    
    def get_nutrition_by_food_id(self, id):
        response = self.get_client().table("food_contains_ingre").select("*, ingredient(name, url_image, id, ingre_contains_nutrition(*))").eq("food_id", id).execute()
        response = response.json()
        response = json.loads(response)
        data = response["data"]
        
        # Từ điển để lưu tổng của từng loại dinh dưỡng
        nutrition_totals = {}

        for ingre in data:
            # Duyệt qua danh sách 'ingre_contains_nutrition'
            for nutrition in ingre['ingredient']['ingre_contains_nutrition']:
                nutrition_id = nutrition['nutrition_id']
                nutrition_amount = nutrition['amount'] * ingre['amount']  # Nhân với lượng nguyên liệu
                
                # Cộng dồn vào từ điển
                if nutrition_id in nutrition_totals:
                    nutrition_totals[nutrition_id] += nutrition_amount
                else:
                    nutrition_totals[nutrition_id] = nutrition_amount
        
        return nutrition_totals

    def vote(self, id, vote):
        response = (
            self.get_client()
            .table("user_Vote_Food")
            .insert([
                {"food_id": id, "user_id": session["user"]["id"], "vote": vote},
            ])
            .execute()
        )
        print("====================")
        print("vote action response")
        print(response)
        print("====================")
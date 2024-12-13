from website.models.basemodel import BaseModel
from website.models.foodmodel import FoodModel
import json
class MealModel(BaseModel):
    def __init__(self):
        super().__init__()

    def insert_meal(self, date, user_id, meal_type, food_id, amount):

        response = (
            self.get_client()
            .table("daily_intake")
            .select("user_id")
            .eq("date", date)
            .eq("user_id", user_id)
            .execute()
        )
        response = response.json()
        response = json.loads(response)
        if response["data"]:
            print("daily_intake already has data -> add total calo")
            print(response["data"])    
        else:
            response = (
                self.get_client()
                .table("daily_intake")
                .insert([
                    {"date": date, "user_id": user_id}
                ])
                .execute()
            )
        # ////////////////////////////////////////////////////////// #
        response = (
            self.get_client()
            .table("meal")
            .select("user_id")
            .eq("date", date)
            .eq("user_id", user_id)
            .eq("meal_type", meal_type)
            .execute()
        )
        response = response.json()
        response = json.loads(response)
        if response["data"]:
            print("daily_intake already has data -> add total calo")
            print(response["data"])
        else:
            response = (
                self.get_client()
                .table("meal")
                .insert([
                    {"date": date, "user_id": user_id, "meal_type": meal_type}
                ])
                .execute()
            )
        id = user_id
        response = (
            self.get_client()
            .table("meal_contains_food")
            .insert([
                {
                    "date": date,
                    "user_id": id,  # Định rõ bảng chứa cột
                    "food_id": food_id,
                    "meal_type": meal_type,
                    "amount": amount,
                }
            ])
            .execute()
        )
        # tính calo 
        food_model = FoodModel()
        nutrition = food_model.get_nutrition_by_food_id(food_id)
        calo = nutrition["Calories"]
        calo = int(calo)
        amount = int(amount)
        # update 2 bảng daily in take và meal 
        total_calories_recent = 0
        response = (
            self.get_client()
            .table("daily_intake")
            .select("totalcalories")
            .eq("date", date)
            .eq("user_id", user_id)
            .execute()
        )
        response = response.json()
        response = json.loads(response)
        total_calories_recent = int(response["data"][0]["totalcalories"])

        response = (
            self.get_client()
            .table("meal")
            .update({"total_calories": (total_calories_recent + calo * amount)})
            .eq("date", date)
            .eq("user_id", user_id)
            .eq("meal_type", meal_type)
            .execute()
        )
        response = (
            self.get_client()
            .table("daily_intake")
            .update({"totalcalories": (total_calories_recent + calo * amount)})
            .eq("date", date)
            .eq("user_id", user_id)
            .execute()
        )
        return response.json()

    def get_all_meal(self, user_id):
        response = (
            self.get_client()
            .table("meal_contains_food")
            .select("*, food(*)")
            .eq("user_id", user_id)
            .execute()
        )
        return response.json()

    def get_all_daily_intake(self, user_id):
        response = (
            self.get_client()
            .table("daily_intake")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return response.json()
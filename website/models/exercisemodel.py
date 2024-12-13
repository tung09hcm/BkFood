from website.models.basemodel import BaseModel
from flask import session # type: ignore
import json
class ExerciseModel(BaseModel):
    def __init__(self):
        super().__init__()

    def get_all_exercises(self):
        response = self.get_client().table("exercise").select("*").execute()
        return response.json()  # Trả về dữ liệu dưới dạng JSON
    
    def user_do_exercise(self,exer_id, user_id, date):
        response = self.get_client().table("user_do_exercise").insert([
            {"exer_id": exer_id, "user_id": user_id, "date": date}
        ]).execute()
        return response.json()
    
    def get_all_exercise_by_userid(self, user_id):
        response = (
            self.get_client()
            .table("user_do_exercise")
            .select("*, exercise(*)")
            .eq("user_id", user_id)
            .execute()
        )
        return response.json()
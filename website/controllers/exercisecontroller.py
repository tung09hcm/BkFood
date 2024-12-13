from website.models.exercisemodel import ExerciseModel
from datetime import datetime
import json
class ExerciseController:
    def __init__(self):
        self.exercise_model = ExerciseModel()

    def get_exercises(self):
        exercises = self.exercise_model.get_all_exercises()
        exercises = json.loads(exercises)
        # Đảm bảo "data" luôn tồn tại
        return exercises["data"]
    
    def user_do_exercise(self,exer_id, user_id):
        date = datetime.now().strftime("%Y-%m-%d")
        exercises = self.exercise_model.user_do_exercise(exer_id, user_id, date)
        exercises = json.loads(exercises)
        return exercises["data"]
    
    def get_all_exercise_by_userid(self, user_id):
        response = self.exercise_model.get_all_exercise_by_userid(user_id)
        response = json.loads(response)
        return response["data"]
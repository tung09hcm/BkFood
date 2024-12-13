from website.models.usermodel import UserModel
import json
class UserController:
    def __init__(self):
        self.user_model = UserModel()

    def add_user(self,username: str, email: str, password: str, age: int, gender: str, height: float, weight: float):
        user = self.user_model.add_user(username,email,password,age,gender,height,weight)
        user = json.loads(user)
        return user["data"]
    
    def login(self, email, password):
        response = self.user_model.verify_user(email, password)
        return response
       
    def update(self,name,email,age,gender,height,weight, id):
        response = self.user_model.update(name,email,age,gender,height,weight, id)
        return response

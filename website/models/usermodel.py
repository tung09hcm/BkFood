from website.models.basemodel import BaseModel
from werkzeug.security import check_password_hash # type: ignore
import json
class UserModel(BaseModel):
    def __init__(self):
        super().__init__()

    def add_user(self, username: str, email: str, password: str, age: int, gender: str, height: int, weight: int):
        """
        Thêm một người dùng mới vào cơ sở dữ liệu Supabase.
        """
        try:
            # Dữ liệu cần chèn vào bảng users
            user_data = {
                "name": username,
                "email": email,
                "password": password,  # Lưu ý: Mật khẩu cần được mã hóa trước khi lưu vào cơ sở dữ liệu.
                "Age": age,
                "Gender": gender.capitalize(),
                "Height": height,
                "Weight": weight
            }
            # Thực hiện chèn dữ liệu vào bảng users
            response = (
                self.get_client()
                .table("user_profile")
                .insert(user_data)
                .execute()
            )

            return response.json()

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"success": False, "message": str(e)}
        
    def verify_user(self, email, password):
        response = self.get_client().table("user_profile").select("*").eq("email", email).execute()
        response = response.json()
        response = json.loads(response)
        user_data = response["data"]
        password_hash_from_db = user_data[0]['password']
        print("user password in usermodel verifyuser:", password_hash_from_db)
        
        if check_password_hash(password_hash_from_db, password):
            print("Mật khẩu đúng!")
            return user_data  # Trả về thông tin người dùng nếu mật khẩu đúng
        else:
            print("Mật khẩu sai!")
            return None


        
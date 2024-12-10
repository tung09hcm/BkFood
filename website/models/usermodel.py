from website.models.basemodel import BaseModel

class UserModel(BaseModel):
    def __init__(self):
        super().__init__()

    def add_user(self, username: str, email: str, password: str, age: int, gender: str, height: float, weight: float):
        """
        Thêm một người dùng mới vào cơ sở dữ liệu Supabase.
        """
        try:
            # Dữ liệu cần chèn vào bảng users
            user_data = {
                "username": username,
                "email": email,
                "password": password,  # Lưu ý: Mật khẩu cần được mã hóa trước khi lưu vào cơ sở dữ liệu.
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight
            }

            # Thực hiện chèn dữ liệu vào bảng users
            response = self.supabase.table("users").insert(user_data).execute()

            # Kiểm tra phản hồi từ Supabase
            if response.status_code == 201:  # 201 là mã phản hồi "Created"
                return {"success": True, "message": "User added successfully.", "data": response.data}
            else:
                return {"success": False, "message": f"Failed to add user: {response.error_message}"}

        except Exception as e:
            return {"success": False, "message": str(e)}
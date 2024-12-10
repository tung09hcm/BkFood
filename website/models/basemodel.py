import os
from supabase import create_client, Client  # type: ignore
from dotenv import load_dotenv # type: ignore

# Tải biến môi trường từ file .env
load_dotenv()

class BaseModel:
    def __init__(self):
        # Lấy thông tin cấu hình từ biến môi trường
        self.SUPABASE_URL = os.getenv("SUPABASE_URL")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        # Kiểm tra nếu biến môi trường không được cấu hình
        if not self.SUPABASE_URL or not self.SUPABASE_KEY:
            raise ValueError("Missing Supabase configuration. Check your .env file.")
        
        # Tạo Supabase client
        self.supabase: Client = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)

    def get_client(self):
        return self.supabase

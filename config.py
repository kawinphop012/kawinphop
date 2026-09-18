import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'super-secret-key-for-social-classroom'
    # ใช้ SQLite และเก็บไฟล์ไว้ที่โฟลเดอร์ instance
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'classroom.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
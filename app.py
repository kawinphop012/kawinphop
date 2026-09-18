import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

# Import Config และ Database
from config import Config
from models.__init__ import db

# Import Models สำหรับสร้างตารางในฐานข้อมูล (เหลือแค่ส่วน User, Classroom, Assignment)
from models.user import User
from models.classroom import ClassRoom, Enrollment
from models.assignment import Assignment, Submission

# Import Blueprints สำหรับจัดการ Routes ต่างๆ
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.classroom import classroom_bp
from routes.assignment import assignment_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # ตั้งค่าระบบ Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # ลงทะเบียนระบบทั้งหมด (Blueprints)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(classroom_bp)
    app.register_blueprint(assignment_bp)
    
    # ตั้งค่าหน้าแรก
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
        
    return app

app = create_app()

def setup_database():
    # สร้างโฟลเดอร์ instance หากยังไม่มี
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    with app.app_context():
        # สร้างตารางทั้งหมดในฐานข้อมูล
        db.create_all()
        
        # สร้างบัญชีตัวอย่างถ้ายังไม่มีในระบบ
        if not User.query.filter_by(email='teacher@test.com').first():
            teacher = User(name='ครูสมชาย', email='teacher@test.com', 
                           password_hash=generate_password_hash('123456'), role='teacher')
            student = User(name='กวินภพ', email='student@test.com', 
                           password_hash=generate_password_hash('123456'), role='student')
            db.session.add(teacher)
            db.session.add(student)
            db.session.commit()
            print("สร้างผู้ใช้ตัวอย่างและฐานข้อมูลสำเร็จ!")

if __name__ == '__main__':
    setup_database()
    app.run(debug=True, port=5000)
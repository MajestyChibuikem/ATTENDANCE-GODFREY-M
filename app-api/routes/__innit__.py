from flask import Blueprint
from routes.auth import auth_bp
from routes.attendance import attendance_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(attendance_bp, url_prefix='/users.py')

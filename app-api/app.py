from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import sqlite3
import os



load_dotenv()
app = Flask(__name__)
# this key is random for now
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Load JWT secret key from .env
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Initialize database
db = SQLAlchemy(app)




from routes.users import users_bp
from routes.attendance import attendance_bp
app.register_blueprint(users_bp, url_prefix = '/api/users')
app.register_blueprint(attendance_bp, url_prefix = '/api/attendance')

if __name__ == "__main__":
    app.run(debug=True)
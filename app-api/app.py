from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import sqlite3
import os



load_dotenv()
app = Flask(__name__)
# this key is random for now
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")
app.config['SQLALCHEMY_DATABASE_URL'] =os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app)

db = SQLAlchemy(app)
# from routes.users
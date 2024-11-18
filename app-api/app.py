from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import sqlite3
import os



load_dotenv()
app = Flask(__name__)
# this key is random for now
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")
jwt = JWTManager(app)

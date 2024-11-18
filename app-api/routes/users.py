from flask import Blueprint, request, jsonify
from models import User

from app import db
users_bp = Blueprint('users', __name__)


@users_bp.route('/Register', methods = ['POST'])
def register():
    data = request.json
    username =  data.get('username')
    password = data.get('password')
    device_key = data.get('device_key')

    if not username or not password or not device_key:
        return jsonify({'error: all fields are required '}), 400
    

    if User.query.filter((User.username == username)| (User.device_key == device_key)):
        return jsonify({'error: user already exists '}), 400
    
    user = User(username = username, device_key = device_key, password = password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message: user registered successfully'}), 201
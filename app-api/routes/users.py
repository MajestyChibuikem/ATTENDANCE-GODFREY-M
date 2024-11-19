from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import User, db

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    device_key = data.get('device_key')

    if not username or not password or not device_key:
        return jsonify({'error': 'All fields are required'}), 400

    if User.query.filter((User.username == username) | (User.device_key == device_key)).first():
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, device_key=device_key)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

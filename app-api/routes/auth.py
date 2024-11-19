from flask import request, Blueprint, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from models import User
from app import db


auth_bp = Blueprint('auth', __name__)

#   user login endpoint
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    check users details and assigns a token if success
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    #   validate
    if not username or not password:
        return jsonify({"error: User Name and Password required"}) ,400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error: username or password invalid"}) ,401
    
    #   generate user tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "message": "login was a success",
        "access token": access_token,
        "refresh token" : refresh_token
    }), 200

#   token refresh
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """
        creates a new access token using the refresh token
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user.id)
    return jsonify({"new access token":new_access_token}), 201
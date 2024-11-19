from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Attendance, User, db
from datetime import date, datetime

attendance_bp = Blueprint('attendance', __name__)

# Mark attendance
@attendance_bp.route('/mark', methods=['POST'])
@jwt_required()
def mark_attendance():
    """
    Marks attendance for the logged-in user for a specific date.
    """
    data = request.json
    user_id = get_jwt_identity()  # Retrieve the current user's ID from JWT
    attendance_date = data.get('date', str(date.today()))
    status = data.get('status', 'Present')

    # Validate date format
    try:
        attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Check if the user exists before marking attendance
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if attendance is already marked for this date
    if Attendance.query.filter_by(user_id=user_id, date=attendance_date).first():
        return jsonify({'error': 'Attendance already marked for this date'}), 400

    # Mark attendance
    attendance = Attendance(user_id=user_id, date=attendance_date, status=status)
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance marked successfully'}), 201

# Get attendance for a user
@attendance_bp.route('/records', methods=['GET'])
@jwt_required()
def get_attendance():
    """
    Retrieves attendance records for the logged-in user between two dates.
    """
    user_id = get_jwt_identity()  # Retrieve the current user's ID from JWT
    start_date = request.args.get('start_date', '2024-11-01')
    end_date = request.args.get('end_date', str(date.today()))

    # Validate date formats
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Check if the user exists before fetching attendance
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Fetch attendance records
    attendance_records = Attendance.query.filter(
        Attendance.user_id == user_id,
        Attendance.date.between(start_date, end_date)
    ).all()

    # Format results
    result = [
        {'date': record.date.isoformat(), 'status': record.status}
        for record in attendance_records
    ]
    return jsonify(result), 200

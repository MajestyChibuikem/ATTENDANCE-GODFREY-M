from flask import Blueprint, request, jsonify
from models import Attendance, User
from app import db
from datetime import date

attendance_bp = Blueprint('attendance', __name__)

# Mark attendance
@attendance_bp.route('/mark', methods=['POST'])
def mark_attendance():
    data = request.json
    user_id = data.get('user_id')
    attendance_date = data.get('date', str(date.today()))
    status = data.get('status', 'Present')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Check if the user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if attendance already marked
    if Attendance.query.filter_by(user_id=user_id, date=attendance_date).first():
        return jsonify({'error': 'Attendance already marked for this date'}), 400

    attendance = Attendance(user_id=user_id, date=attendance_date, status=status)
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance marked successfully'}), 201

# Get attendance for a user
@attendance_bp.route('/<int:user_id>', methods=['GET'])
def get_attendance(user_id):
    start_date = request.args.get('start_date', '2024-11-01')
    end_date = request.args.get('end_date', str(date.today()))

    attendance_records = Attendance.query.filter(
        Attendance.user_id == user_id,
        Attendance.date.between(start_date, end_date)
    ).all()

    result = [
        {'date': record.date.isoformat(), 'status': record.status}
        for record in attendance_records
    ]
    return jsonify(result), 200

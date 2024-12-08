from flask import Blueprint, request, jsonify
from models import db, Employee
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

employee_bp = Blueprint('employee', __name__)
limiter = Limiter(key_func=get_remote_address)

@employee_bp.route('', methods=['POST'])
@limiter.limit("10 per minute")
def create_employee():
    data = request.get_json()
    new_employee = Employee(
        name=data['name'],
        position=data['position']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee created successfully'}), 201

@employee_bp.route('', methods=['GET'])
@limiter.limit("100 per minute")
def get_all_employees():
    employees = Employee.query.all()
    return jsonify([{
        'id': emp.id,
        'name': emp.name,
        'position': emp.position
    } for emp in employees]), 200

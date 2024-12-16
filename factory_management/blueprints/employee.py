from flask import Blueprint, jsonify, request
from factory_management.models import db, Employee

# Define the employee blueprint
employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['name', 'position', 'salary']):
            return jsonify({"error": "Missing required fields"}), 400

        new_employee = Employee(
            name=data['name'],
            position=data['position'],
            salary=data['salary']
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"message": "Employee created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_bp.route('/', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    if employees:
        return jsonify([{
            "id": emp.id,
            "name": emp.name,
            "position": emp.position,
            "salary": emp.salary
        } for emp in employees]), 200
    return jsonify({"message": "No employees found"}), 404

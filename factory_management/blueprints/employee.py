from flask import Blueprint, jsonify
from factory_management.models import db, Employee

# Define the employee blueprint
employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    if employees:
        return jsonify([employee.to_dict() for employee in employees]), 200
    return jsonify({"message": "No employees found"}), 404

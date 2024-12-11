from flask import Blueprint, jsonify, request
from factory_management.models import db, Employee

# Define the employee blueprint
employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/', methods=['GET', 'POST'])
def get_employees():
    if request.method == 'POST':
        return jsonify({"message": "Method not allowed"}), 405
    employees = Employee.query.all()
    if employees:
        return jsonify([employee.to_dict() for employee in employees]), 200
    return jsonify({"message": "No employees found"}), 404

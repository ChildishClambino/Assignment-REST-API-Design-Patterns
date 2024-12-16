from flask import Blueprint, request, jsonify
from factory_management.models import db, Customer

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

customer_bp = Blueprint('customer', __name__)
limiter = Limiter(key_func=get_remote_address)

@customer_bp.route('/', methods=['POST'])
@limiter.limit("10 per minute")
def create_customer():
    data = request.get_json()
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

@customer_bp.route('/', methods=['GET'])
@limiter.limit("100 per minute")
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': cust.id,
        'name': cust.name,
        'email': cust.email,
        'phone': cust.phone
    } for cust in customers]), 200
from flask import Blueprint, request, jsonify
from factory_management.models import db, Order

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

order_bp = Blueprint('order', __name__)
limiter = Limiter(key_func=get_remote_address)

@order_bp.route('', methods=['POST'])
@limiter.limit("10 per minute")
def create_order():
    data = request.get_json()
    new_order = Order(
        customer_id=data['customer_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=data['total_price']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@order_bp.route('', methods=['GET'])
@limiter.limit("100 per minute")
def get_all_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': order.id,
        'customer_id': order.customer_id,
        'product_id': order.product_id,
        'quantity': order.quantity,
        'total_price': order.total_price
    } for order in orders]), 200
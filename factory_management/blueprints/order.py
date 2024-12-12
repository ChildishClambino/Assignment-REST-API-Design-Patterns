from flask import Blueprint, request, jsonify
from factory_management.models import db, Order
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
order_bp = Blueprint('order', __name__)

@order_bp.route('/', methods=['POST'])
@limiter.limit("10 per minute")
def create_order():
    data = request.get_json()
    required_fields = ['customer_id', 'product_id', 'quantity', 'total_price']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f"Missing required fields: {', '.join(missing_fields)}"}), 400

    new_order = Order(
        customer_id=data['customer_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=data['total_price']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully.'}), 201

@order_bp.route('/', methods=['GET'])
@limiter.limit("5 per minute")
def get_all_orders():
    """Get all orders."""
    orders = Order.query.all()
    print("Orders fetched in endpoint:", orders)  # Debug print
    if not orders:  # No orders found
        return jsonify([]), 200  # Return an empty list with 200
    return jsonify([order.to_dict() for order in orders]), 200

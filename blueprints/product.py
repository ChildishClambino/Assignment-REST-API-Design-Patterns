from flask import Blueprint, request, jsonify
from models import db, Product
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

product_bp = Blueprint('product', __name__)
limiter = Limiter(key_func=get_remote_address)

@product_bp.route('', methods=['POST'])
@limiter.limit("10 per minute")
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@product_bp.route('', methods=['GET'])
@limiter.limit("100 per minute")
def get_all_products():
    products = Product.query.all()
    return jsonify([{
        'id': prod.id,
        'name': prod.name,
        'price': prod.price
    } for prod in products]), 200
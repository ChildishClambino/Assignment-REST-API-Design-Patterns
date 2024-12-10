from flask import Blueprint, request, jsonify
from factory_management.models import db, Product

from factory_management.utils.util import token_required, role_required

product_bp = Blueprint('product', __name__)

@product_bp.route('', methods=['POST'])
@token_required
@role_required('admin')
def create_product(decoded_token):
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@product_bp.route('', methods=['GET'])
@token_required
def get_all_products(decoded_token):
    products = Product.query.all()
    return jsonify([{
        'id': prod.id,
        'name': prod.name,
        'price': prod.price
    } for prod in products]), 200
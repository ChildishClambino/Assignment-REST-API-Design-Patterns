from flask import Blueprint, request, jsonify
from factory_management.models import db, Production
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime

production_bp = Blueprint('production', __name__)
limiter = Limiter(key_func=get_remote_address)

@production_bp.route('', methods=['POST'])
@limiter.limit("10 per minute")
def create_production():
    data = request.get_json()
    if not data or not all(key in data for key in ['product_id', 'quantity_produced', 'date_produced']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_production = Production(
            product_id=data['product_id'],
            quantity_produced=data['quantity_produced'],
            date_produced=datetime.strptime(data['date_produced'], '%Y-%m-%d').date()
        )
        db.session.add(new_production)
        db.session.commit()
        return jsonify({'message': 'Production record created successfully'}), 201
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400


@production_bp.route('', methods=['GET'])
@limiter.limit("100 per minute")
def get_all_production():
    productions = Production.query.all()
    if not productions:
        return jsonify({'message': 'No production records found'}), 404

    return jsonify([{
        'id': prod.id,
        'product_id': prod.product_id,
        'quantity_produced': prod.quantity_produced,
        'date_produced': str(prod.date_produced)
    } for prod in productions]), 200
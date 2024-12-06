from factory import create_app
from flask import request, jsonify
from models import Order, Product, db

app = create_app()

# Pagination for Orders
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate pagination parameters
        if page < 1 or per_page < 1:
            return jsonify({'message': 'Invalid pagination parameters. Both page and per_page must be positive integers.'}), 400

        orders = Order.query.paginate(page=page, per_page=per_page, error_out=False)
        if not orders.items:
            return jsonify({'message': 'No orders found on this page.'}), 404

        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': orders.page
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

# Pagination for Products
@app.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    
    if not products.items:
        return jsonify({'message': 'No products found on this page.'}), 404
    
    return jsonify({
        'products': [product.to_dict() for product in products.items],
        'total': products.total,
        'pages': products.pages,
        'current_page': products.page
    })

# Analyze Employee Performance
@app.route('/employee_performance', methods=['GET'])
def analyze_employee_performance():
    results = db.session.query(
        Order.employee_name,
        db.func.sum(Order.quantity).label('total_quantity')
    ).group_by(Order.employee_name).all()

    return jsonify([{'employee_name': r.employee_name, 'total_quantity': int(r.total_quantity)} for r in results])

@app.route('/top_selling_products', methods=['GET'])
def top_selling_products():
    results = db.session.query(
        Product.name,
        db.func.sum(Order.quantity).label('total_quantity')
    ).join(Order, Order.product_id == Product.id).group_by(Product.name).order_by(db.desc('total_quantity')).all()

    return jsonify([{'product_name': r.name, 'total_quantity': int(r.total_quantity)} for r in results])


# Determine Customer Lifetime Value
@app.route('/customer_lifetime_value', methods=['GET'])
def customer_lifetime_value():
    threshold = request.args.get('threshold', 100, type=float)
    results = db.session.query(
        Order.customer_id,
        db.func.sum(Order.total_value).label('total_value')
    ).group_by(Order.customer_id).having(db.func.sum(Order.total_value) >= threshold).all()

    if not results:
        return jsonify({'message': 'No customers found with lifetime value exceeding the threshold.'}), 404

    return jsonify([{'customer_id': r.customer_id, 'total_value': float(r.total_value)} for r in results])


# Evaluate Production Efficiency
@app.route('/production_efficiency', methods=['GET'])
def production_efficiency():
    specific_date = request.args.get('date')
    
    if not specific_date:
        return jsonify({'message': 'Date parameter is required.'}), 400

    try:
        subquery = db.session.query(
            Order.product_id,
            db.func.sum(Order.quantity).label('total_quantity')
        ).filter(Order.date == specific_date).group_by(Order.product_id).subquery()

        results = db.session.query(
            Product.name,
            subquery.c.total_quantity
        ).join(subquery, Product.id == subquery.c.product_id).all()

        if not results:
            return jsonify({'message': 'No production data found for the specified date.'}), 404

        return jsonify([{'product_name': r.name, 'total_quantity': int(r.total_quantity)} for r in results])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(debug=True)

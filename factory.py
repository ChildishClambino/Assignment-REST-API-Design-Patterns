from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db
from config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Register blueprints
    from blueprints.employee import employee_bp
    from blueprints.product import product_bp
    from blueprints.order import order_bp
    from blueprints.customer import customer_bp
    from blueprints.production import production_bp
    
    app.register_blueprint(employee_bp, url_prefix='/api/employees')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(production_bp, url_prefix='/api/production')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
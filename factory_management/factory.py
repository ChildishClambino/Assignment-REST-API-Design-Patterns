from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from factory_management.models import db
from factory_management.config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CORS(app)  # Enable CORS for all routes

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    # Import and register blueprints
    from factory_management.blueprints.employee import employee_bp
    from factory_management.blueprints.product import product_bp
    from factory_management.blueprints.order import order_bp
    from factory_management.blueprints.customer import customer_bp
    from factory_management.blueprints.production import production_bp
    from factory_management.swagger_documentation import swagger_bp

    # Register blueprints with conflict checks
    if 'employee_bp' not in app.blueprints:
        app.register_blueprint(employee_bp, url_prefix='/api/employees')
    if 'product_bp' not in app.blueprints:
        app.register_blueprint(product_bp, url_prefix='/api/products')
    if 'order_bp' not in app.blueprints:
        app.register_blueprint(order_bp, url_prefix='/api/orders')
    if 'customer_bp' not in app.blueprints:
        app.register_blueprint(customer_bp, url_prefix='/api/customers')
    if 'production_bp' not in app.blueprints:
        app.register_blueprint(production_bp, url_prefix='/api/productions')
    if 'swagger' not in app.blueprints:
        app.register_blueprint(swagger_bp, url_prefix='/api/docs')

    # Ensure database tables are created
    with app.app_context():
        db.create_all()

    return app

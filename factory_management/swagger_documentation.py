from flask import Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import os
import json

# Define Blueprint
swagger_bp = Blueprint('swagger', __name__, static_folder='static')

# Swagger configuration
SWAGGER_URL = '/api/docs'  # URL for accessing Swagger UI
API_URL = '/api/docs/swagger.json'  # URL for accessing Swagger JSON

# Initialize Swagger UI Blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Factory Management System API"}
)

# Avoid nested prefixes by directly registering routes
swagger_bp.register_blueprint(swaggerui_blueprint, url_prefix='')

# Static folder path
static_dir = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(static_dir, exist_ok=True)

# Define Swagger documentation content
swagger_content = {
    "swagger": "2.0",
    "info": {
        "title": "Factory Management System API",
        "description": "API documentation for managing factory operations.",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "paths": {
        "/api/employees/": {
            "get": {
                "summary": "List Employees",
                "description": "Retrieve all employees",
                "responses": {
                    "200": {
                        "description": "List of employees",
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "name": {"type": "string"},
                                    "position": {"type": "string"},
                                    "salary": {"type": "number"}
                                }
                            }
                        }
                    },
                    "404": {"description": "No employees found"}
                }
            },
            "post": {
                "summary": "Create Employee",
                "description": "Add a new employee to the system",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "position": {"type": "string"},
                                "salary": {"type": "number"}
                            },
                            "required": ["name", "position", "salary"]
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Employee created successfully"},
                    "400": {"description": "Invalid input"}
                }
            }
        },
        "/api/products/": {
            "get": {
                "summary": "List Products",
                "description": "Retrieve all products",
                "responses": {
                    "200": {
                        "description": "List of products",
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "name": {"type": "string"},
                                    "price": {"type": "number"}
                                }
                            }
                        }
                    },
                    "404": {"description": "No products found"}
                }
            },
            "post": {
                "summary": "Create Product",
                "description": "Add a new product to the system",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "price": {"type": "number"}
                            },
                            "required": ["name", "price"]
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Product created successfully"},
                    "400": {"description": "Invalid input"}
                }
            }
        },
        "/api/orders/": {
            "get": {
                "summary": "List Orders",
                "description": "Retrieve all orders",
                "responses": {
                    "200": {
                        "description": "List of orders",
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "customer_id": {"type": "integer"},
                                    "product_id": {"type": "integer"},
                                    "quantity": {"type": "integer"},
                                    "total_price": {"type": "number"}
                                }
                            }
                        }
                    },
                    "404": {"description": "No orders found"}
                }
            },
            "post": {
                "summary": "Create Order",
                "description": "Place a new order",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "customer_id": {"type": "integer"},
                                "product_id": {"type": "integer"},
                                "quantity": {"type": "integer"},
                                "total_price": {"type": "number"}
                            },
                            "required": ["customer_id", "product_id", "quantity", "total_price"]
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Order placed successfully"},
                    "400": {"description": "Invalid input"}
                }
            }
        },
        "/api/customers/": {
            "get": {
                "summary": "List Customers",
                "description": "Retrieve all customers",
                "responses": {
                    "200": {
                        "description": "List of customers",
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "name": {"type": "string"},
                                    "email": {"type": "string"},
                                    "phone": {"type": "string"}
                                }
                            }
                        }
                    },
                    "404": {"description": "No customers found"}
                }
            },
            "post": {
                "summary": "Create Customer",
                "description": "Add a new customer to the system",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "email": {"type": "string"},
                                "phone": {"type": "string"}
                            },
                            "required": ["name", "email", "phone"]
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Customer created successfully"},
                    "400": {"description": "Invalid input"}
                }
            }
        },
        "/api/productions/": {
            "get": {
                "summary": "List Productions",
                "description": "Retrieve all productions",
                "responses": {
                    "200": {
                        "description": "List of productions",
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "product_id": {"type": "integer"},
                                    "quantity": {"type": "integer"},
                                    "date_produced": {"type": "string", "format": "date"}
                                }
                            }
                        }
                    },
                    "404": {"description": "No productions found"}
                }
            },
            "post": {
                "summary": "Create Production",
                "description": "Log a new production",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "integer"},
                                "quantity": {"type": "integer"},
                                "date_produced": {"type": "string", "format": "date"}
                            },
                            "required": ["product_id", "quantity", "date_produced"]
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Production logged successfully"},
                    "400": {"description": "Invalid input"}
                }
            }
        }
    }
}

# Write Swagger JSON
swagger_json_path = os.path.join(static_dir, 'swagger.json')
with open(swagger_json_path, 'w') as f:
    json.dump(swagger_content, f, indent=4)

# Swagger JSON Route
@swagger_bp.route('/swagger.json', methods=['GET'])
def swagger_json():
    return jsonify(swagger_content)
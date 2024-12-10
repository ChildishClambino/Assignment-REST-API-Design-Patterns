import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from factory_management.config import Config

SECRET_KEY = Config.SECRET_KEY

# Function to encode a token
def encode_token(user_id, role):
    """
    Generates a JWT token with the user's ID and role.
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=1),  
            'iat': datetime.utcnow(),                      
            'sub': str(user_id),                           
            'role': role                                   
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        raise ValueError(f"Error encoding token: {e}")
    
# Function to decode a token
def decode_token(token):
    """
    Decodes a JWT token and returns the payload if valid.
    """
    try:
        print(f"Decoding token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(f"Decoded payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        print("Error: Token expired")
        return {'error': 'Token expired. Please log in again.'}
    except jwt.InvalidTokenError as e:
        print(f"Error: {e}")
        return {'error': 'Invalid token. Please log in again.'}

# Decorator to check if a valid token is provided
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            print("Token is missing!")
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            print(f"Raw token from header: {token}")
            token = token.split(" ")[1]  #  this removes 'Bearer' prefix
            print(f"Token after split: {token}")
            decoded_token = decode_token(token)
            print(f"Decoded token: {decoded_token}")
            if 'error' in decoded_token:
                return jsonify(decoded_token), 401
        except Exception as e:
            print(f"Error during token validation: {e}")
            return jsonify({'message': str(e)}), 401
        return f(decoded_token, *args, **kwargs)
    return decorated

# Decorator to validate role-based access
def role_required(role):
    """
    Checks if the decoded token has the specified role.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(decoded_token, *args, **kwargs):
            if decoded_token.get('role') != role:
                return jsonify({'message': 'Permission denied!'}), 403
            return f(decoded_token, *args, **kwargs)
        return decorated_function
    return decorator
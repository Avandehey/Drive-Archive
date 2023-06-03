from flask import request, jsonify
from functools import wraps
from app.models import User

def token_required(flask_route):
    @wraps(flask_route)
    def wrapper(*args, **kwargs):
        # Check if 'x-access-token' is present in the request headers
        if 'x-access-token' in request.headers:
            # Extract the token from the request headers
            try:
                token = request.headers['x-access-token'].split()[1]
                # Query the User table for a user with the given token
                user = User.query.filter_by(token=token).first()
                
                if user:
                    # Call the original flask_route with the user object
                    return flask_route(user, *args, **kwargs)
                
                return jsonify({"message": "Invalid Token"}), 401
            except:
                return jsonify({"message": "Invalid Token"}), 401
        return jsonify([{'message': 'Missing Token'}]), 401
    return wrapper

from flask import request, jsonify

from . import bp
from app.models import User

# Verify user
@bp.post('/verifyuser')
def verify_user():
    content = request.json
    username = content['username']
    password = content['password']
    
    # Query the User table for a user with the given username
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        return jsonify([{'user token': user.token}])
    return jsonify({'message': 'Invalid username or password'})

# Register User
@bp.post('/register-user')
def register_user():
    content = request.json
    username = content['username']
    email = content['email']
    password = content['password']
    
    # Query the User table for a user with the given username
    user = User.query.filter_by(username=username).first()
    
    if user:
        return jsonify([{'message': 'Username Taken, Try again'}])
    
    # Query the User table for a user with the given email
    user = User.query.filter_by(email=email).first()
    
    if user:
        return jsonify([{'message': 'Email Taken, Try again'}])
    
    # Create a new User object with the given email and username
    user = User(email=email, username=username)
    user.password = user.hash_password(password)
    user.add_token()
    user.commit()
    print(user)
    return jsonify([{'message': f"{user.username} Registered"}])

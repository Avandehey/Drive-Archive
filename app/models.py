from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from secrets import token_urlsafe

from app import db, login

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    username = db.Column(db.String(60), unique=True)  # User's username (max length: 60)
    email = db.Column(db.String(100), unique=True)  # User's email (max length: 100)
    password = db.Column(db.String(200))  # User's hashed password
    token = db.Column(db.String(250), unique=True)  # Token for user authentication
    post = db.relationship('Post', backref='author', lazy=True)  # Relationship with posts

    def __repr__(self):
        return f'User: {self.username}'

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def hash_password(self, password):
        return generate_password_hash(password)  # Hashes the given password using Werkzeug's generate_password_hash function

    def check_password(self, password):
        return check_password_hash(self.password, password)  # Checks if the given password matches the hashed password

    def add_token(self):
        setattr(self, 'token', token_urlsafe(32))  # Generates a random URL-safe token and assigns it to the user's token attribute

    def get_id(self):
        return str(self.user_id)  # Returns the string representation of the user's ID

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each post
    body = db.Column(db.String(250))  # Content of the post (max length: 250)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())  # Timestamp of when the post was created
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Foreign key referencing the user who authored the post

    def __repr__(self):
        return f'<Post: {self.body}>'

    def commit(self):
        db.session.add(self)
        db.session.commit()

from flask import request, jsonify

from . import bp
from app.models import Post, User
from app.blueprints.api.helpers import token_required

# Receive All Posts
@bp.get('/posts')
@token_required
def api_posts(user):
    result = []
    posts = Post.query.all()
    for post in posts:
        result.append({
            'id': post.id,
            'body': post.body,
            'timestamp': post.timestamp,
            'author': post.user_id
        })
    return jsonify(result), 200

# Receive Posts from Single User
@bp.get('/posts/<username>')
@token_required
def user_posts(user, username):
    # Query the User table for the user with the given username
    user = User.query.filter_by(username=username).first()
    
    if user:
        return jsonify([{
            'id': post.id,
            'body': post.body,
            'timestamp': post.timestamp,
            'author': post.user_id
        } for post in user.post]), 200
    return jsonify({'message': 'Invalid Username'}), 404

# Send single post
@bp.get('/post/<post_id>')
@token_required
def get_post(user, post_id):
    try:
        # Query the Post table for the post with the given post_id
        post = Post.query.get(post_id)
        return jsonify([{
            'id': post.id,
            'body': post.body,
            'timestamp': post.timestamp,
            'author': post.user_id
        }])
    except:
        return jsonify({'message': 'Invalid Post Id'}), 404

# Make a Post
@bp.post('/post')
@token_required
def make_post(user):
    try:
        content = request.json
        # Create a new Post object with the given body and user_id
        post = Post(body=content.get('body'), user_id=user.user_id)
        post.commit()
        return jsonify([{'message': 'Post Created', 'body': post.body}])
    except:
        return jsonify([{'message': 'Invalid form data'}]), 401

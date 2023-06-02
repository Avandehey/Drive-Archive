from flask import request, jsonify

from . import bp
from app.models import Post, User

# Recieve All Posts
@bp.get('/posts')
def api_posts():
    result = []
    posts = Post.query.all()
    for post in posts:
        result.append({
            'id':post.id,
            'body':post.body,
            'timestamp':post.timestamp,
            'author':post.user_id
        })
    return jsonify(result), 200

# Recieve Posts from Single User
@bp.get('/posts/<username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify([{
                'id':post.id,
                'body':post.body,
                'timestamp':post.timestamp,
                'author':post.user_id
                } for post in user.post]), 200
    return jsonify({'message':'Invalid Username'}) , 404

# Send single post

@bp.get('/post/<id>')
def get_post(id):
    try:
        post = Post.query.get(id)
        return jsonify([{
                'id':post.id,
                'body':post.body,
                'timestamp':post.timestamp,
                'author':post.user_id
                }])
    except:
        return jsonify({'message':'Invalid Post Id'}) , 404 

# Make a Post


from app import app
from app.models import Post, User
from flask import jsonify

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    data = {'items': [post.to_dict() for post in posts]}
    return jsonify(data)

@app.route('/api/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_dict())
    
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    data = {'items': [user.to_dict() for user in users]}
    return jsonify(data)

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@app.route('/api/users/<int:id>/followers', methods=['GET'])
def get_user_followers(id):
    user = User.query.get_or_404(id)
    followers = user.followers.all()
    return jsonify({'followers': [follower.to_dict() for follower in followers]})

@app.route('/api/users/<int:id>/followed', methods=['GET'])
def get_user_followed(id):
    user = User.query.get_or_404(id)
    followed_users = user.followed.all()
    return jsonify({'followed': [followed_user.to_dict() for followed_user in followed_users]})
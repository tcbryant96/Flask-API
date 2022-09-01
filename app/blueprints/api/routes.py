from . import api
from flask import jsonify, request
from app.models import Post, User

@api.route('/')
def index():
    names = ['Brian', 'Tatyana', 'Nate', 'Sam']
    return jsonify(names)    

@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@api.route('/posts/<id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_dict())

@api.route('/posts', methods=["POST"]) # post request
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    
    # get the data from the request body
    data = request.json
    print(data, type(data))
    for field in ['title', 'body', 'user_id']:
        if field not in data:
            # if field not in request body, respond with a 400 error
            return jsonify({'error': f'{field} must be in request body'}), 400
            # error is the response and 400 is the server error
    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')

    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201

@api.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for user in ['username', 'email','password']:
        if user not in data:
            return jsonify({'error': f'{user} must be in request body'}), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get("password")
    new_user= User(username=username, email=email, password=password)
    return jsonify(new_user.to_dict()), 201



@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@api.route('/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())


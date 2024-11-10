from flask import Flask, request, jsonify
import jwt
import datetime
from pymongo import MongoClient
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
app.config['SECRET_KEY'] = 'your_secret_key'  #SUGGEST_CHANGE

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/') #SUGGEST_CHANGE # Replace with your MongoDB URI #'mongodb+srv://<username>:<password>@cluster0.mongodb.net/mydatabase'
db = client['mydatabase']
users = db['users']


#SUGGEST_CHANGE - Move permission and auth helpers to say a middleware.py
# groups and permission key value
PERMISSIONS = {
    'admin': ['admin_permission'], # add more permission on the list
    'standard': ['standard_permission']
}

def getUserPermissions(user):
    all_permission = []
    user_groups = user.get('groups', [])
    for group in user_groups:
        all_permission.extend(PERMISSIONS.get(group))
    return set(all_permission)

# Utility functions
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = users.find_one({"username": data['username']})
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def check_permission(required_permissions):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
             # Check if the user has at least one of the required permissions
            if not any(permission in getUserPermissions(current_user) for permission in required_permissions):
                return jsonify({'message': 'Permission denied!'}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

#SUGGEST_CHANGE - Create a blueprints for other routes
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({'ping': 'pong'})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    existing_user = users.find_one({"username": data['username']})
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    
    hashed_password = generate_password_hash(data['password'])

    #SUGGEST_CHANGE - Create a model class for User
    users.insert_one({
        "username": data['username'],
        "password": hashed_password,
        "groups": ['admin'],
    })
    return jsonify({'message': 'Registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users.find_one({"username": data['username']})
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = jwt.encode({
        'username': user['username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

@app.route('/api/admin_permission', methods=['GET'])
@token_required
@check_permission(['admin_permission'])
def admin_permission(current_user):
    return jsonify({'message': 'Admin permission granted'})

@app.route('/api/standard_permission', methods=['GET'])
@token_required
@check_permission(['standard_permission'])
def standard_permission(current_user):
    return jsonify({'message': 'Standard permission granted'})

@app.route('/api/admin_standard_permission', methods=['GET'])
@token_required
@check_permission(['standard_permission', 'admin_permission'])
def admin_standard_permission(current_user):
    return jsonify({'message': 'Admin and Standard permission granted'})

@app.route('/api/user/me', methods=['GET'])
@token_required
def general_access(current_user):
    return jsonify({
        'username': current_user['username'],
        'groups': current_user['groups'],
    })


if __name__ == '__main__':
    app.run(port=8000, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "sequoalpha-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simple in-memory database
users_db = {}
user_id_counter = 1

def create_default_admin():
    global user_id_counter
    admin_password = get_password_hash("admin123")
    admin_user = {
        "id": user_id_counter,
        "username": "admin",
        "email": "admin@sequoalpha.com",
        "full_name": "SequoAlpha Administrator",
        "hashed_password": admin_password,
        "is_active": True,
        "is_admin": True
    }
    users_db["admin"] = admin_user
    user_id_counter += 1

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def get_current_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except jwt.InvalidTokenError:
        return None
    
    user = users_db.get(username)
    if user is None:
        return None
    return user

def get_current_admin(token):
    user = get_current_user(token)
    if not user or not user.get("is_admin"):
        return None
    return user

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"detail": "Username and password required"}), 400
    
    user = users_db.get(username)
    if not user:
        return jsonify({"detail": "Incorrect username or password"}), 401
    
    if not verify_password(password, user["hashed_password"]):
        return jsonify({"detail": "Incorrect username or password"}), 401
    
    if not user["is_active"]:
        return jsonify({"detail": "Inactive user"}), 400
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return jsonify({"access_token": access_token, "token_type": "bearer"})

@app.route('/admin/create-user', methods=['POST'])
def create_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Admin token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_admin = get_current_admin(token)
    if not current_admin:
        return jsonify({"detail": "Admin privileges required"}), 403
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    
    if not username or not email or not password:
        return jsonify({"detail": "Username, email and password required"}), 400
    
    global user_id_counter
    
    if username in users_db:
        return jsonify({"detail": "Username already exists"}), 400
    
    for existing_user in users_db.values():
        if existing_user["email"] == email:
            return jsonify({"detail": "Email already exists"}), 400
    
    hashed_password = get_password_hash(password)
    
    new_user = {
        "id": user_id_counter,
        "username": username,
        "email": email,
        "full_name": full_name,
        "hashed_password": hashed_password,
        "is_active": True,
        "is_admin": False
    }
    
    users_db[username] = new_user
    user_id_counter += 1
    
    return jsonify({
        "id": new_user["id"],
        "username": new_user["username"],
        "email": new_user["email"],
        "full_name": new_user["full_name"],
        "is_active": new_user["is_active"]
    })

@app.route('/users/me', methods=['GET'])
def read_users_me():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_user = get_current_user(token)
    if not current_user:
        return jsonify({"detail": "Invalid token"}), 401
    
    return jsonify({
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "is_active": current_user["is_active"]
    })

@app.route('/dashboard', methods=['GET'])
def dashboard():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_user = get_current_user(token)
    if not current_user:
        return jsonify({"detail": "Invalid token"}), 401
    
    return jsonify({
        "message": "Welcome to SequoAlpha Management Dashboard",
        "user": current_user["username"],
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "SequoAlpha Management API - Secure Access Only"})

# Initialize default admin user
create_default_admin()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

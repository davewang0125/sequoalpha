from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import bcrypt
import os
import uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "sequoalpha-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simple in-memory database
users_db = {}
user_id_counter = 1

# Documents database
documents_db = {}
document_id_counter = 1

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        "is_active": current_user["is_active"],
        "is_admin": current_user["is_admin"]
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

# Document management endpoints
@app.route('/admin/documents', methods=['GET'])
def get_documents():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_user = get_current_user(token)
    if not current_user:
        return jsonify({"detail": "Invalid token"}), 401
    
    # Get filter parameters
    category = request.args.get('category', 'All')
    
    documents = list(documents_db.values())
    
    # Filter by category if specified
    if category != 'All':
        documents = [doc for doc in documents if doc['category'] == category]
    
    # Calculate statistics
    total_documents = len(documents_db)
    new_this_month = len([doc for doc in documents_db.values() 
                         if doc['created_at'].month == datetime.utcnow().month])
    categories = len(set(doc['category'] for doc in documents_db.values()))
    last_updated = max([doc['created_at'] for doc in documents_db.values()]).strftime('%b %d') if documents_db else 'Never'
    
    return jsonify({
        "documents": documents,
        "statistics": {
            "total_documents": total_documents,
            "new_this_month": new_this_month,
            "categories": categories,
            "last_updated": last_updated
        }
    })

@app.route('/admin/documents/upload', methods=['POST'])
def upload_document():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Admin token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_admin = get_current_admin(token)
    if not current_admin:
        return jsonify({"detail": "Admin privileges required"}), 403
    
    if 'file' not in request.files:
        return jsonify({"detail": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"detail": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"detail": "Only PDF files are allowed"}), 400
    
    # Get form data
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    category = request.form.get('category', 'Other')
    
    if not title:
        return jsonify({"detail": "Title is required"}), 400
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    
    # Save file
    file.save(file_path)
    
    # Get file size
    file_size = os.path.getsize(file_path)
    file_size_mb = round(file_size / (1024 * 1024), 1)
    
    # Create document record
    global document_id_counter
    document = {
        "id": document_id_counter,
        "title": title,
        "description": description,
        "category": category,
        "type": "PDF",
        "filename": unique_filename,
        "file_size": f"{file_size_mb} MB",
        "is_external": False,
        "external_url": None,
        "created_at": datetime.utcnow(),
        "is_new": True
    }
    
    documents_db[document_id_counter] = document
    document_id_counter += 1
    
    return jsonify(document)

@app.route('/admin/documents/link', methods=['POST'])
def add_document_link():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Admin token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_admin = get_current_admin(token)
    if not current_admin:
        return jsonify({"detail": "Admin privileges required"}), 403
    
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    category = data.get('category', 'Other')
    external_url = data.get('external_url')
    
    if not title or not external_url:
        return jsonify({"detail": "Title and URL are required"}), 400
    
    # Create document record
    global document_id_counter
    document = {
        "id": document_id_counter,
        "title": title,
        "description": description,
        "category": category,
        "type": "LINK",
        "filename": None,
        "file_size": "N/A",
        "is_external": True,
        "external_url": external_url,
        "created_at": datetime.utcnow(),
        "is_new": True
    }
    
    documents_db[document_id_counter] = document
    document_id_counter += 1
    
    return jsonify(document)

@app.route('/admin/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Admin token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_admin = get_current_admin(token)
    if not current_admin:
        return jsonify({"detail": "Admin privileges required"}), 403
    
    if document_id not in documents_db:
        return jsonify({"detail": "Document not found"}), 404
    
    document = documents_db[document_id]
    
    # Delete file if it exists
    if document['filename'] and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], document['filename'])):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], document['filename']))
    
    # Remove from database
    del documents_db[document_id]
    
    return jsonify({"message": "Document deleted successfully"})

@app.route('/documents/<filename>', methods=['GET'])
def download_document(filename):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_user = get_current_user(token)
    if not current_user:
        return jsonify({"detail": "Invalid token"}), 401
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "SequoAlpha Management API - Secure Access Only"})

def create_sample_documents():
    global document_id_counter
    sample_docs = [
        {
            "id": document_id_counter,
            "title": "Q2 2025 Performance Report",
            "description": "Quarterly performance review and market analysis",
            "category": "Reports",
            "type": "PDF",
            "filename": "sample_report.pdf",
            "file_size": "2.4 MB",
            "is_external": False,
            "external_url": None,
            "created_at": datetime.utcnow(),
            "is_new": True
        },
        {
            "id": document_id_counter + 1,
            "title": "Meridian Growth Fund Factsheet",
            "description": "Fund overview, strategy, and key metrics",
            "category": "Factsheets",
            "type": "PDF",
            "filename": "factsheet.pdf",
            "file_size": "1.2 MB",
            "is_external": False,
            "external_url": None,
            "created_at": datetime.utcnow(),
            "is_new": True
        },
        {
            "id": document_id_counter + 2,
            "title": "Limited Partnership Agreement",
            "description": "Terms and conditions of partnership",
            "category": "Legal",
            "type": "PDF",
            "filename": "agreement.pdf",
            "file_size": "3.8 MB",
            "is_external": False,
            "external_url": None,
            "created_at": datetime.utcnow(),
            "is_new": False
        },
        {
            "id": document_id_counter + 3,
            "title": "Monthly Market Commentary",
            "description": "August market insights and outlook",
            "category": "Reports",
            "type": "LINK",
            "filename": None,
            "file_size": "N/A",
            "is_external": True,
            "external_url": "https://example.com/market-commentary.pdf",
            "created_at": datetime.utcnow(),
            "is_new": True
        }
    ]
    
    for doc in sample_docs:
        documents_db[doc["id"]] = doc
        document_id_counter += 1

create_default_admin()
create_sample_documents()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

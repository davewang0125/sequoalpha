from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import bcrypt
import os
import uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from models import db, User, Document

load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080", "http://localhost:3000", "https://your-netlify-domain.netlify.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Database configuration
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///sequoalpha.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    return user

def get_current_admin(token):
    user = get_current_user(token)
    if not user or not user.is_admin:
        return None
    return user

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"detail": "Username and password required"}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"detail": "Incorrect username or password"}), 401
    
    if not verify_password(password, user.hashed_password):
        return jsonify({"detail": "Incorrect username or password"}), 401
    
    if not user.is_active:
        return jsonify({"detail": "Inactive user"}), 400
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
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
    
    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"detail": "Username already exists"}), 400
    
    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"detail": "Email already exists"}), 400
    
    hashed_password = get_password_hash(password)
    
    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict())

@app.route('/admin/change-password', methods=['POST'])
def change_password():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Admin token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_admin = get_current_admin(token)
    if not current_admin:
        return jsonify({"detail": "Admin privileges required"}), 403
    
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')
    
    if not username or not new_password:
        return jsonify({"detail": "Username and new password required"}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"detail": "User not found"}), 404
    
    user.hashed_password = get_password_hash(new_password)
    db.session.commit()
    
    return jsonify({"message": f"Password updated successfully for user {username}"})

@app.route('/admin/users', methods=['GET'])
def get_users():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Admin token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_admin = get_current_admin(token)
    if not current_admin:
        return jsonify({"detail": "Admin privileges required"}), 403
    
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    
    return jsonify({"users": users_list})

@app.route('/users/me', methods=['GET'])
def read_users_me():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_user = get_current_user(token)
    if not current_user:
        return jsonify({"detail": "Invalid token"}), 401
    
    return jsonify(current_user.to_dict())



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
    
    # Query documents
    if category != 'All':
        documents = Document.query.filter_by(category=category).all()
    else:
        documents = Document.query.all()
    
    # Calculate statistics
    total_documents = Document.query.count()
    new_this_month = Document.query.filter(
        Document.created_at >= datetime.utcnow().replace(day=1)
    ).count()
    categories = db.session.query(Document.category).distinct().count()
    last_doc = Document.query.order_by(Document.created_at.desc()).first()
    last_updated = last_doc.created_at.strftime('%b %d') if last_doc else 'Never'
    
    return jsonify({
        "documents": [doc.to_dict() for doc in documents],
        "statistics": {
            "total_documents": total_documents,
            "new_this_month": new_this_month,
            "categories": categories,
            "last_updated": last_updated
        }
    })

# User document access endpoint (for regular users)
@app.route('/documents', methods=['GET'])
def get_user_documents():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_user = get_current_user(token)
    if not current_user:
        return jsonify({"detail": "Invalid token"}), 401
    
    # Get filter parameters
    category = request.args.get('category', 'All')
    
    # Query documents (same as admin but without statistics)
    if category != 'All':
        documents = Document.query.filter_by(category=category).all()
    else:
        documents = Document.query.all()
    
    return jsonify([doc.to_dict() for doc in documents])

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
    document = Document(
        title=title,
        description=description,
        category=category,
        type="PDF",
        filename=unique_filename,
        file_size=f"{file_size_mb} MB",
        is_external=False,
        external_url=None,
        is_new=True,
        created_by=current_admin.id
    )
    
    db.session.add(document)
    db.session.commit()
    
    return jsonify(document.to_dict())

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
    document = Document(
        title=title,
        description=description,
        category=category,
        type="LINK",
        filename=None,
        file_size="N/A",
        is_external=True,
        external_url=external_url,
        is_new=True,
        created_by=current_admin.id
    )
    
    db.session.add(document)
    db.session.commit()
    
    return jsonify(document.to_dict())

@app.route('/admin/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Admin token required"}), 401
    
    token = auth_header.split(' ')[1]
    current_admin = get_current_admin(token)
    if not current_admin:
        return jsonify({"detail": "Admin privileges required"}), 403
    
    document = Document.query.get(document_id)
    if not document:
        return jsonify({"detail": "Document not found"}), 404
    
    # Delete file if it exists
    if document.filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], document.filename)):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], document.filename))
    
    # Remove from database
    db.session.delete(document)
    db.session.commit()
    
    return jsonify({"message": "Document deleted successfully"})

@app.route('/admin/documents/<int:document_id>/download', methods=['GET'])
def download_document_by_id(document_id):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"detail": "Token required"}), 401
        
        token = auth_header.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "Invalid token"}), 401
        
        # Get document from database
        document = Document.query.get(document_id)
        if not document:
            return jsonify({"detail": "Document not found"}), 404
        
        if not document.filename:
            return jsonify({"detail": "No file associated with this document"}), 400
        
        # Check if file exists
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], document.filename)
        if not os.path.exists(file_path):
            return jsonify({"detail": "File not found"}), 404
        
        # Set proper headers for file download
        response = send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            document.filename, 
            as_attachment=True,
            download_name=document.title.replace(' ', '_') + '.pdf'
        )
        
        # Add CORS headers for download
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        
        return response
        
    except Exception as e:
        print(f"Download error: {str(e)}")
        return jsonify({"detail": "Download failed"}), 500

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)

# SequoAlpha Management LLC

A secure authentication system with FastAPI backend and React frontend for SequoAlpha Management LLC.

## 🚀 Features

- **FastAPI Backend**: Modern, fast Python web framework
- **JWT Authentication**: Secure token-based authentication
- **React Frontend**: Modern, responsive user interface
- **Login Only**: Secure login system (no public registration)
- **Admin User Management**: Only admins can create new users
- **Simple Dashboard**: Basic dashboard for authenticated users
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

```
sequoalpha/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── js/
│       ├── App.js          # Main React component
│       ├── Login.js        # Login component
│       ├── Dashboard.js    # Dashboard component
│       ├── App.css         # App styles
│       ├── Login.css       # Login styles
│       └── Dashboard.css   # Dashboard styles
├── index.html              # Main login page
├── images/                 # Background images
├── css/                    # Additional styles
└── README.md               # This file
```

## 🛠️ Installation & Setup

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd sequoalpha/backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI server:**
   ```bash
   python main.py
   ```

   The API will be available at: http://localhost:8000

### Frontend Setup

1. **Open the main page:**
   - Simply open `index.html` in your web browser
   - Or serve it with a local server:
     ```bash
     python -m http.server 3000
     ```
     Then visit: http://localhost:3000

## 🔧 API Endpoints

### Authentication
- `POST /login` - Login user
- `GET /users/me` - Get current user info (protected)

### Admin Routes (Admin Only)
- `POST /admin/create-user` - Create new user (admin only)

### Dashboard
- `GET /dashboard` - Access dashboard data (protected)

## 🔑 Default Admin Credentials

The system creates a default admin user:
- **Username**: `admin`
- **Password**: `admin123`

**⚠️ IMPORTANT**: Change these credentials in production!

## 🎯 Usage

1. **Start the backend server** (see Backend Setup above)
2. **Open the frontend** in your browser
3. **Login** with admin credentials or user credentials provided by admin
4. **Access the dashboard** with your authenticated session

### Creating New Users (Admin Only)

Only admin users can create new users. Use the admin endpoint:

```bash
curl -X POST "http://localhost:8000/admin/create-user" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "New User"
  }'
```

## 🔒 Security Features

- **JWT Tokens**: Secure authentication tokens
- **Password Hashing**: Bcrypt password encryption
- **Admin-Only User Creation**: No public registration
- **CORS Protection**: Cross-origin resource sharing configuration
- **Input Validation**: Pydantic model validation
- **Error Handling**: Comprehensive error responses

## 🎨 Frontend Features

- **Modern UI**: Clean, professional design matching SequoAlpha branding
- **Responsive**: Works on all device sizes
- **Form Validation**: Client-side validation
- **Loading States**: User feedback during operations
- **Error Handling**: Clear error messages
- **Background Integration**: Uses same background as main site

## 🚀 Development

### Adding New Features

1. **Backend**: Add new endpoints in `main.py`
2. **Frontend**: Create new React components in `frontend/js/`
3. **Styling**: Add CSS in the appropriate component file

### Database Integration

The current implementation uses an in-memory database. To integrate with a real database:

1. Add database dependencies to `requirements.txt`
2. Replace the `users_db` dictionary with database models
3. Update the authentication functions to use the database

## 📝 Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
```

## 🔧 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend is running on the correct port
2. **Module Not Found**: Make sure all dependencies are installed
3. **Port Already in Use**: Change the port in `main.py` or kill the existing process

### Getting Help

- Check the browser console for frontend errors
- Check the terminal for backend errors
- Ensure both frontend and backend are running

## 📄 License

This project is for SequoAlpha Management LLC internal use.

## 📞 Contact

- **Address**: 319 N Bernardo Ave, Mountainview, CA 94043
- **Phone**: 650-308-9049
- **Email**: info@sequoalpha.com

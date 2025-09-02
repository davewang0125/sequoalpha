# Deployment Guide - SequoAlpha Management

## 🚀 How to Deploy to Your Host

### Option 1: Simple File Upload (Recommended for Static Hosting)

1. **Upload the frontend files:**
   - Upload the entire `frontend/` folder to your web host
   - Make sure `login.html` is accessible at your domain

2. **Update the API URL:**
   - Edit `frontend/js/Login.js` and `frontend/js/Dashboard.js`
   - Change `http://localhost:8000` to your backend API URL
   - Example: `https://your-api-domain.com`

3. **Deploy the backend separately:**
   - Upload the `backend/` folder to your server
   - Install Python dependencies
   - Run the FastAPI server

### Option 2: Complete Server Deployment

1. **Upload all files to your server**
2. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   echo "SECRET_KEY=your-super-secret-production-key" > .env
   ```

4. **Run the backend:**
   ```bash
   python main.py
   ```

5. **Configure your web server to serve the frontend**

## 🔧 Configuration for Production

### Backend Configuration

1. **Change the default admin password:**
   - Edit `backend/main.py`
   - Find the line: `admin_password = get_password_hash("admin123")`
   - Change "admin123" to a secure password

2. **Set a strong SECRET_KEY:**
   ```bash
   echo "SECRET_KEY=your-very-long-random-secret-key" > .env
   ```

3. **Configure CORS for your domain:**
   - Edit `backend/main.py`
   - Update the CORS origins to your domain:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-domain.com"],  # Your domain
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

### Frontend Configuration

1. **Update API endpoints:**
   - Edit `frontend/js/Login.js` line 25:
   ```javascript
   const response = await fetch('https://your-api-domain.com/login', {
   ```
   
   - Edit `frontend/js/Dashboard.js` line 15:
   ```javascript
   const response = await fetch('https://your-api-domain.com/protected', {
   ```

## 📁 File Structure for Upload

```
your-host/
├── login.html          # Main login page
├── js/
│   ├── App.js         # Main React app
│   ├── Login.js       # Login component
│   ├── Dashboard.js   # Dashboard component
│   ├── App.css        # App styles
│   ├── Login.css      # Login styles
│   └── Dashboard.css  # Dashboard styles
└── images/            # Background images (if needed)
```

## 🔒 Security Checklist

- [ ] Changed default admin password
- [ ] Set strong SECRET_KEY
- [ ] Configured CORS for your domain
- [ ] Updated API URLs in frontend
- [ ] Enabled HTTPS
- [ ] Set up proper firewall rules

## 🌐 Domain Configuration

### For the Frontend:
- Point your domain to the folder containing `login.html`
- Ensure all CSS and JS files are accessible

### For the Backend:
- Set up a subdomain or separate domain for the API
- Configure reverse proxy (nginx/Apache) to forward requests to the FastAPI server
- Example: `api.yourdomain.com` → FastAPI server

## 📞 Support

If you need help with deployment, contact:
- **Email**: info@sequoalpha.com
- **Phone**: 650-308-9049

## 🔄 Updates

To update the system:
1. Upload new frontend files
2. Restart the backend server
3. Clear browser cache if needed

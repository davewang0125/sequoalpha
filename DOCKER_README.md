# 🐳 Docker Local Testing Guide

This guide helps you test the SequoAlpha application locally using Docker before deploying to EC2.

## 📋 Prerequisites

- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)
- 4GB+ RAM available for Docker

## 🚀 Quick Start

### 1. Start All Services

```bash
# From the project root directory
docker-compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- Flask backend (port 8000)
- Nginx frontend (port 8080)

### 2. Access the Application

Open your browser to: **http://localhost:8080**

- **Admin Login**: `admin` / `admin123`
- **User Login**: `user` / `user123`

### 3. Stop Services

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (clean slate)
docker-compose down -v
```

## 📦 Docker Architecture

```
┌─────────────────────────────────────────┐
│          Your Browser                   │
│      http://localhost:8080              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│     Frontend (Nginx)                     │
│     Container: sequoalpha-frontend       │
│     Port: 8080 → 80                      │
│                                          │
│  • Serves static files                   │
│  • Proxies /api to backend               │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│     Backend (Flask + Gunicorn)           │
│     Container: sequoalpha-backend        │
│     Port: 8000                           │
│                                          │
│  • Flask application                     │
│  • JWT authentication                    │
│  • Document management                   │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│     Database (PostgreSQL)                │
│     Container: sequoalpha-postgres       │
│     Port: 5432                           │
│                                          │
│  • User data                             │
│  • Document metadata                     │
└──────────────────────────────────────────┘
```

## 🔧 Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

### Execute Commands in Containers

```bash
# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec postgres psql -U sequoalpha_user -d sequoalpha

# Run Python commands
docker-compose exec backend python -c "print('Hello')"
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up --build

# Rebuild specific service
docker-compose up --build backend
```

## 🧪 Testing Scenarios

### Test 1: Basic Functionality

1. Start services: `docker-compose up`
2. Open http://localhost:8080
3. Login as admin
4. Create a new user
5. Upload a document
6. Download the document
7. ✅ Success if all steps work

### Test 2: Database Persistence

```bash
# Create data
docker-compose up
# Login and create users/documents

# Stop containers
docker-compose down

# Restart (data should persist)
docker-compose up
# ✅ Your data should still be there
```

### Test 3: API Endpoints

```bash
# Test backend directly
curl http://localhost:8000/

# Test CORS
curl http://localhost:8000/test-cors

# Test through nginx
curl http://localhost:8080/api/
```

### Test 4: File Uploads

1. Login as admin
2. Upload a PDF document
3. Check backend logs: `docker-compose logs backend`
4. Verify upload: `docker-compose exec backend ls -la uploads/`
5. Download the document
6. ✅ File should download correctly

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# - Database not ready: Wait 10 seconds and retry
# - Port 8000 in use: Stop other services using port 8000
```

### Database connection errors

```bash
# Check if postgres is healthy
docker-compose ps

# Should show postgres as "healthy"
# If not, wait a few seconds for initialization

# Test connection
docker-compose exec postgres pg_isready -U sequoalpha_user
```

### Frontend shows 404 or connection errors

```bash
# Check if backend is responding
curl http://localhost:8000/

# Check nginx logs
docker-compose logs frontend

# Verify config
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
```

### Port already in use

```bash
# Find what's using the port
lsof -i :8080  # For frontend
lsof -i :8000  # For backend
lsof -i :5432  # For postgres

# Stop the conflicting service or change port in docker-compose.yml
```

### Clean start (nuclear option)

```bash
# Stop everything
docker-compose down -v

# Remove all sequoalpha images
docker images | grep sequoalpha | awk '{print $3}' | xargs docker rmi -f

# Rebuild from scratch
docker-compose up --build
```

## 🔍 Inspecting the System

### Check Container Status

```bash
docker-compose ps
```

### View Resource Usage

```bash
docker stats
```

### Inspect Database

```bash
# Connect to database
docker-compose exec postgres psql -U sequoalpha_user -d sequoalpha

# List tables
\dt

# View users
SELECT * FROM users;

# View documents
SELECT * FROM documents;

# Exit
\q
```

### View Files in Containers

```bash
# Backend uploads
docker-compose exec backend ls -la uploads/

# Frontend files
docker-compose exec frontend ls -la /usr/share/nginx/html/
```

## 📝 Development Workflow

### Making Code Changes

The Docker setup is configured with volume mounts for live development:

1. **Backend changes**: Edit files in `backend/`
   - Container will auto-reload (using `--reload` flag)
   - No rebuild needed for Python changes

2. **Frontend changes**: Edit files in `frontend/`, `css/`, etc.
   - Changes are immediately reflected
   - Just refresh browser

3. **Configuration changes**: Edit nginx config or Dockerfiles
   - Requires rebuild: `docker-compose up --build`

### Testing Like Production

To test in production-like mode:

```bash
# Edit docker-compose.yml
# Change FLASK_DEBUG to False
# Remove --reload from command

docker-compose down
docker-compose up --build
```

## 🔐 Environment Variables

To test with AWS S3 or other services:

1. Edit `docker-compose.yml`
2. Uncomment and fill in environment variables:
   ```yaml
   - AWS_ACCESS_KEY_ID=your-key
   - AWS_SECRET_ACCESS_KEY=your-secret
   - AWS_REGION=us-east-1
   - AWS_S3_BUCKET_NAME=your-bucket
   ```
3. Restart: `docker-compose up --build`

## 📊 Performance Testing

### Load Testing

```bash
# Install Apache Bench (if not already installed)
# macOS: brew install apache-bench
# Ubuntu: sudo apt-get install apache2-utils

# Test login endpoint
ab -n 100 -c 10 http://localhost:8000/test-cors

# Test frontend
ab -n 100 -c 10 http://localhost:8080/
```

## 🎯 What This Tests

✅ **Database connectivity** - PostgreSQL integration  
✅ **Backend API** - All Flask endpoints  
✅ **Frontend serving** - Nginx configuration  
✅ **API proxying** - Nginx → Backend communication  
✅ **File uploads** - Document management  
✅ **Authentication** - JWT token handling  
✅ **Static files** - CSS, JS, images  
✅ **CORS** - Cross-origin requests  
✅ **Container networking** - Service communication  

## 🚀 Differences from EC2 Deployment

| Aspect | Docker (Local) | EC2 (Production) |
|--------|----------------|------------------|
| **Database** | Container | EC2 or RDS |
| **Backend** | Container | Systemd service |
| **Frontend** | Container | Nginx on host |
| **Networking** | Bridge network | EC2 network |
| **Storage** | Volumes | Local + S3 |
| **Ports** | 8080 | 80/443 |
| **SSL** | No | Yes (Let's Encrypt) |

## ✨ Next Steps

After successfully testing with Docker:

1. ✅ Everything works locally
2. 📝 Read EC2_DEPLOYMENT.md
3. 🚀 Deploy to EC2 with confidence
4. 🎉 Your app is production-ready!

## 🔄 Continuous Testing

Add this to your development workflow:

```bash
# Before committing code
docker-compose down -v
docker-compose up --build
# Run tests
# Commit if all tests pass
```

## 📞 Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Check container status: `docker-compose ps`
3. Check this troubleshooting section
4. Review Docker Desktop resources (increase if needed)

---

**Happy Testing!** 🐳

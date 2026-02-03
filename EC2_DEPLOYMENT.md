# 🚀 EC2 Deployment Guide for SequoAlpha Management System

This guide will help you deploy the SequoAlpha Management System to an AWS EC2 instance.

## 📋 Prerequisites

- AWS Account with EC2 access
- EC2 instance running Ubuntu 20.04 or 22.04 LTS
- Domain name (optional, but recommended)
- SSH access to your EC2 instance

## 🏗️ Architecture Overview

```
Internet → EC2 Instance
          ├── Nginx (Port 80/443) → Frontend (Static Files)
          │                      → Backend API (Port 8000)
          ├── Gunicorn (Port 8000) → Flask Application
          ├── PostgreSQL (Local or RDS)
          └── S3 (File Storage)
```

## 🔧 Step 1: EC2 Instance Setup

### 1.1 Launch EC2 Instance

1. Go to AWS EC2 Console
2. Click "Launch Instance"
3. Choose **Ubuntu Server 22.04 LTS** AMI
4. Instance type: **t2.small** or **t2.medium** (recommended)
5. Configure Security Group:
   - SSH (22) - Your IP only
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
   - Custom TCP (8000) - 0.0.0.0/0 (for testing, remove in production)
6. Launch and save your `.pem` key file

### 1.2 Connect to EC2

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

## 🛠️ Step 2: Install Dependencies

Run the automated setup script or follow manual steps below:

### Option A: Automated Setup (Recommended)

```bash
# Upload and run the deployment script
chmod +x deploy_ec2.sh
sudo ./deploy_ec2.sh
```

### Option B: Manual Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Nginx
sudo apt install -y nginx

# Install Git
sudo apt install -y git

# Install build essentials (needed for some Python packages)
sudo apt install -y build-essential libpq-dev
```

## 📦 Step 3: Setup Application

### 3.1 Clone Repository

```bash
cd /home/ubuntu
git clone https://github.com/yourusername/sequoalpha.git
cd sequoalpha
```

### 3.2 Setup Backend

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
nano .env
```

Add the following to `.env`:

```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=production
FLASK_DEBUG=False

# Database Configuration
DATABASE_URL=postgresql://sequoalpha_user:your_password@localhost/sequoalpha

# AWS S3 Configuration (Optional but recommended)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-bucket-name

# Server Configuration
PORT=8000
```

### 3.3 Setup PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE sequoalpha;
CREATE USER sequoalpha_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE sequoalpha TO sequoalpha_user;
ALTER DATABASE sequoalpha OWNER TO sequoalpha_user;
\q

# Initialize database
cd /home/ubuntu/sequoalpha/backend
source venv/bin/activate
python init_db.py
```

## ⚙️ Step 4: Configure Systemd Service

Create a systemd service to run the backend automatically:

```bash
sudo nano /etc/systemd/system/sequoalpha.service
```

Add the configuration (see `sequoalpha.service` file).

```bash
# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl start sequoalpha
sudo systemctl enable sequoalpha

# Check status
sudo systemctl status sequoalpha
```

## 🌐 Step 5: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/sequoalpha
```

Add the nginx configuration (see `nginx.conf` file).

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/sequoalpha /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

## 🔐 Step 6: SSL/HTTPS Setup (Optional but Recommended)

### Using Let's Encrypt (Free SSL)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is set up automatically
# Test renewal
sudo certbot renew --dry-run
```

## 🗄️ Step 7: Setup AWS S3 (Recommended)

Follow the instructions in `AWS_S3_SETUP.md` to:
1. Create S3 bucket
2. Create IAM user with S3 access
3. Add credentials to `.env` file

## 📊 Step 8: Monitoring and Logs

### View Application Logs

```bash
# Backend logs
sudo journalctl -u sequoalpha -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Manage Service

```bash
# Start service
sudo systemctl start sequoalpha

# Stop service
sudo systemctl stop sequoalpha

# Restart service
sudo systemctl restart sequoalpha

# Check status
sudo systemctl status sequoalpha
```

## 🔄 Step 9: Deploy Updates

Create a deployment script:

```bash
cd /home/ubuntu/sequoalpha

# Pull latest changes
git pull origin main

# Backend updates
cd backend
source venv/bin/activate
pip install -r requirements.txt
python init_db.py  # If database schema changed

# Restart service
sudo systemctl restart sequoalpha

# Restart nginx (if frontend changed)
sudo systemctl restart nginx
```

## 🧪 Step 10: Testing

### Test Backend API

```bash
curl http://your-ec2-ip/api/
```

### Test Frontend

Open in browser: `http://your-ec2-ip`

### Test Full Flow

1. Login with default credentials:
   - Admin: `admin` / `admin123`
   - User: `user` / `user123`
2. Upload a document
3. Download a document
4. Create a new user (admin only)

## 🔒 Security Best Practices

1. **Change Default Passwords**
   ```bash
   # Login to your app and change admin password immediately
   ```

2. **Update .env SECRET_KEY**
   ```bash
   # Generate a new secret key
   python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
   ```

3. **Restrict SSH Access**
   - Update EC2 Security Group to allow SSH only from your IP
   - Consider using AWS Systems Manager Session Manager

4. **Setup Firewall**
   ```bash
   sudo ufw allow OpenSSH
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

5. **Regular Updates**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

6. **Database Backups**
   ```bash
   # Automated backup script
   pg_dump sequoalpha > backup_$(date +%Y%m%d).sql
   ```

## 🐛 Troubleshooting

### Backend not starting

```bash
# Check logs
sudo journalctl -u sequoalpha -n 50

# Check if port 8000 is in use
sudo lsof -i :8000

# Verify .env file
cat /home/ubuntu/sequoalpha/backend/.env
```

### Database connection errors

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U sequoalpha_user -d sequoalpha -h localhost
```

### Nginx errors

```bash
# Check nginx configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log
```

### File upload issues

```bash
# Check uploads directory permissions
ls -la /home/ubuntu/sequoalpha/backend/uploads

# Fix permissions if needed
sudo chown -R ubuntu:ubuntu /home/ubuntu/sequoalpha/backend/uploads
chmod 755 /home/ubuntu/sequoalpha/backend/uploads
```

## 📝 Estimated Costs

- **EC2 t2.small**: ~$17/month
- **EC2 t2.medium**: ~$34/month
- **Elastic IP**: Free (if associated)
- **PostgreSQL RDS** (optional): Starting at ~$15/month
- **S3 Storage**: ~$0.023/GB/month
- **Data Transfer**: First 1GB free, then ~$0.09/GB

**Total Estimated**: $20-50/month depending on configuration

## 🎯 Next Steps

1. Setup automated backups
2. Configure CloudWatch monitoring
3. Setup auto-scaling (if needed)
4. Configure Route 53 for domain management
5. Setup CI/CD pipeline with GitHub Actions

## 📞 Support

For issues or questions:
- Check logs: `sudo journalctl -u sequoalpha -f`
- Review nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Check database: `sudo -u postgres psql sequoalpha`

---

© 2025 SequoAlpha Management LP. All rights reserved.

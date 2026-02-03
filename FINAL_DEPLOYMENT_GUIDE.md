# 🚀 Final EC2 Deployment Guide

This is your step-by-step guide to deploy SequoAlpha to AWS EC2.

## ✅ Pre-Deployment Checklist

Before you begin, make sure you have:
- [ ] AWS Account with EC2 access
- [ ] Domain name (optional, can use EC2 IP)
- [ ] AWS credentials for S3 (optional but recommended)
- [ ] SSH key pair for EC2 access

## 📋 Step 1: Launch EC2 Instance

### 1.1 Create EC2 Instance
1. Go to AWS EC2 Console → Launch Instance
2. **Name**: `sequoalpha-production`
3. **AMI**: Ubuntu Server 22.04 LTS (64-bit x86)
4. **Instance Type**: t2.small (minimum) or t2.medium (recommended)
5. **Key Pair**: Create new or use existing
6. **Network Settings** - Create security group with these rules:
   - SSH (22) - Your IP only
   - HTTP (80) - 0.0.0.0/0 (Anywhere)
   - HTTPS (443) - 0.0.0.0/0 (Anywhere)
7. **Storage**: 20 GB gp3 (minimum)
8. Click "Launch Instance"

### 1.2 Connect to Your Instance
```bash
# Make your key file secure
chmod 400 your-key.pem

# Connect to EC2 (replace with your IP and key file)
ssh -i your-key.pem ubuntu@YOUR-EC2-PUBLIC-IP
```

## 📦 Step 2: Deploy Application

### 2.1 Clone Repository
```bash
cd /home/ubuntu
git clone https://github.com/YOUR-USERNAME/sequoalpha.git
cd sequoalpha
```

### 2.2 Run Automated Deployment
```bash
chmod +x deploy_ec2.sh
sudo ./deploy_ec2.sh
```

The script will:
- ✅ Update system packages
- ✅ Install Python 3.11, PostgreSQL, Nginx
- ✅ Create database and user
- ✅ Setup Python virtual environment
- ✅ Install Python dependencies
- ✅ Create .env file template
- ✅ Initialize database with sample data
- ✅ Configure systemd service
- ✅ Configure Nginx
- ✅ Setup firewall

## ⚙️ Step 3: Configure Environment

### 3.1 Update Backend Environment Variables
```bash
nano /home/ubuntu/sequoalpha/backend/.env
```

**CRITICAL - Update these values:**
```bash
# Generate a strong secret key
SECRET_KEY=YOUR_RANDOM_SECRET_KEY_HERE

# Update database password
DATABASE_URL=postgresql://sequoalpha_user:YOUR_SECURE_PASSWORD@localhost/sequoalpha

# For CORS - use '*' for same-server deployment (EC2)
CORS_ORIGINS=*

# Optional: Add S3 credentials for file storage
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-bucket-name
```

**Generate SECRET_KEY:**
```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
```

### 3.2 Update Database Password
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Change password (replace YOUR_SECURE_PASSWORD)
ALTER USER sequoalpha_user WITH PASSWORD 'YOUR_SECURE_PASSWORD';
\q
```

### 3.3 Update Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/sequoalpha
```

Replace `your-domain.com` with:
- Your actual domain name (if you have one), OR
- Your EC2 public IP address

Example:
```nginx
server_name 54.123.45.67;  # Your EC2 IP
# OR
server_name myapp.com www.myapp.com;  # Your domain
```

## 🔄 Step 4: Restart Services

```bash
# Restart backend
sudo systemctl restart sequoalpha

# Restart Nginx
sudo systemctl restart nginx

# Check status
sudo systemctl status sequoalpha
sudo systemctl status nginx
```

## 🧪 Step 5: Test Deployment

### 5.1 Test Backend API
```bash
curl http://localhost:8000/
```

Should return: `{"message": "SequoAlpha API is running"}`

### 5.2 Test Frontend
Open in your browser:
```
http://YOUR-EC2-PUBLIC-IP
```

You should see the login page.

### 5.3 Test Login
**Default Credentials:**
- Admin: `admin` / `admin123`
- User: `user` / `user123`

**⚠️ IMPORTANT: Change these passwords immediately after first login!**

## 🔒 Step 6: Security Hardening

### 6.1 Change Default Passwords
1. Login as admin
2. Go to Admin → User Management
3. Change admin password
4. Create new admin user
5. Delete or disable default users

### 6.2 Setup HTTPS with Let's Encrypt (Recommended)
```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Follow the prompts
# Certbot will automatically configure Nginx for HTTPS
```

### 6.3 Verify Firewall
```bash
sudo ufw status
```

Should show:
- 22/tcp (SSH) - ALLOW
- 80/tcp (HTTP) - ALLOW
- 443/tcp (HTTPS) - ALLOW

### 6.4 Regular Updates
```bash
# Update system packages monthly
sudo apt update && sudo apt upgrade -y
```

## 📊 Step 7: Monitoring and Maintenance

### View Logs
```bash
# Backend logs (live)
sudo journalctl -u sequoalpha -f

# Nginx access logs
sudo tail -f /var/log/nginx/sequoalpha_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/sequoalpha_error.log
```

### Service Management
```bash
# Using the management script
./manage.sh status    # Check status
./manage.sh logs      # View logs
./manage.sh restart   # Restart services
./manage.sh backup    # Backup database

# Or use systemctl directly
sudo systemctl restart sequoalpha
sudo systemctl stop sequoalpha
sudo systemctl start sequoalpha
```

### Database Backup
```bash
# Manual backup
sudo -u postgres pg_dump sequoalpha > backup_$(date +%Y%m%d).sql

# Or use the script
./manage.sh backup
```

## 🔄 Step 8: Deploying Updates

When you push new code:

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@YOUR-EC2-IP

# Navigate to app directory
cd /home/ubuntu/sequoalpha

# Run update script
./update.sh
```

The script will:
1. Pull latest code from git
2. Update Python dependencies
3. Run database migrations
4. Restart backend service
5. Restart Nginx

## 🌍 Step 9: Domain Setup (Optional)

If you have a domain name:

### 9.1 Point Domain to EC2
1. Go to your domain registrar (e.g., GoDaddy, Namecheap)
2. Update DNS records:
   - **A Record**: `@` → Your EC2 Public IP
   - **A Record**: `www` → Your EC2 Public IP
3. Wait for DNS propagation (5-30 minutes)

### 9.2 Update Nginx
```bash
sudo nano /etc/nginx/sites-available/sequoalpha
```

Update `server_name` with your domain:
```nginx
server_name yourdomain.com www.yourdomain.com;
```

### 9.3 Get SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 🐛 Troubleshooting

### Backend Not Starting
```bash
# Check logs
sudo journalctl -u sequoalpha -n 50

# Check if port is in use
sudo lsof -i :8000

# Verify .env file
cat /home/ubuntu/sequoalpha/backend/.env
```

### Database Connection Errors
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U sequoalpha_user -d sequoalpha -h localhost

# Check database exists
sudo -u postgres psql -l
```

### 502 Bad Gateway
```bash
# Check if backend is running
sudo systemctl status sequoalpha

# Check Nginx error logs
sudo tail -f /var/log/nginx/sequoalpha_error.log

# Verify backend is listening
curl http://localhost:8000/
```

### File Upload Issues
```bash
# Check uploads directory permissions
ls -la /home/ubuntu/sequoalpha/backend/uploads

# Fix permissions
sudo chown -R ubuntu:ubuntu /home/ubuntu/sequoalpha/backend/uploads
chmod 755 /home/ubuntu/sequoalpha/backend/uploads
```

### CORS Errors
Make sure in `/home/ubuntu/sequoalpha/backend/.env`:
```bash
CORS_ORIGINS=*
```

Then restart:
```bash
sudo systemctl restart sequoalpha
```

## 💰 Estimated Monthly Costs

- **EC2 t2.small**: ~$17/month
- **EC2 t2.medium**: ~$34/month
- **S3 Storage**: ~$0.023/GB/month
- **Data Transfer**: First 1GB free, then ~$0.09/GB
- **Total**: $20-50/month (depending on usage)

## 📞 Support

### Useful Commands
```bash
# Check all services
./manage.sh status

# View real-time logs
./manage.sh logs

# Test connectivity
./manage.sh test

# Restart everything
./manage.sh restart

# Create backup
./manage.sh backup
```

### Log Locations
- Backend: `sudo journalctl -u sequoalpha`
- Nginx Access: `/var/log/nginx/sequoalpha_access.log`
- Nginx Error: `/var/log/nginx/sequoalpha_error.log`
- Database: `sudo -u postgres psql sequoalpha`

## ✅ Post-Deployment Checklist

After deployment, verify:
- [ ] Can access frontend at http://YOUR-EC2-IP
- [ ] Can login with default credentials
- [ ] Changed all default passwords
- [ ] Backend API is responding
- [ ] Can upload documents
- [ ] Can download documents
- [ ] HTTPS is configured (if using domain)
- [ ] Backups are configured
- [ ] Monitoring is working

## 🎉 You're Done!

Your SequoAlpha Management System is now live on EC2!

**Next Steps:**
1. Share the URL with your team
2. Create user accounts
3. Upload documents
4. Setup automated backups
5. Configure monitoring alerts

---

© 2025 SequoAlpha Management LP. All rights reserved.

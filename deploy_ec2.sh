#!/bin/bash

# SequoAlpha EC2 Deployment Script
# This script automates the deployment of SequoAlpha Management System on EC2
# Usage: sudo ./deploy_ec2.sh

set -e  # Exit on error

echo "🚀 SequoAlpha EC2 Deployment Script"
echo "===================================="
echo ""

# Check if running as root/sudo
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root or with sudo"
    exit 1
fi

# Variables
APP_DIR="/home/ubuntu/sequoalpha"
BACKEND_DIR="$APP_DIR/backend"
VENV_DIR="$BACKEND_DIR/venv"
LOG_DIR="/var/log/sequoalpha"

echo "📦 Step 1: Updating system packages..."
apt update && apt upgrade -y

echo "🐍 Step 2: Installing Python and dependencies..."
apt install -y python3.11 python3.11-venv python3-pip
apt install -y build-essential libpq-dev

echo "🗄️ Step 3: Installing PostgreSQL..."
apt install -y postgresql postgresql-contrib

echo "🌐 Step 4: Installing Nginx..."
apt install -y nginx

echo "📥 Step 5: Installing Git..."
apt install -y git

echo "🔧 Step 6: Installing additional tools..."
apt install -y curl wget vim ufw

# Setup PostgreSQL
echo "💾 Step 7: Setting up PostgreSQL database..."
sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname = 'sequoalpha'" | grep -q 1 || \
sudo -u postgres psql <<EOF
CREATE DATABASE sequoalpha;
CREATE USER sequoalpha_user WITH PASSWORD 'changeme_in_production';
GRANT ALL PRIVILEGES ON DATABASE sequoalpha TO sequoalpha_user;
ALTER DATABASE sequoalpha OWNER TO sequoalpha_user;
EOF

echo "✅ PostgreSQL database created"

# Check if app directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "❌ Application directory not found: $APP_DIR"
    echo "📝 Please clone your repository first:"
    echo "   cd /home/ubuntu"
    echo "   git clone https://github.com/yourusername/sequoalpha.git"
    exit 1
fi

# Setup Python virtual environment
echo "🐍 Step 8: Setting up Python virtual environment..."
cd "$BACKEND_DIR"
python3.11 -m venv venv
source venv/bin/activate

echo "📦 Step 9: Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo "📝 Step 10: Creating .env file..."
    cat > "$BACKEND_DIR/.env" <<EOF
# Flask Configuration
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
FLASK_ENV=production
FLASK_DEBUG=False

# Database Configuration
DATABASE_URL=postgresql://sequoalpha_user:changeme_in_production@localhost/sequoalpha

# AWS S3 Configuration (Optional - add your credentials)
# AWS_ACCESS_KEY_ID=your-aws-access-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret-key
# AWS_REGION=us-east-1
# AWS_S3_BUCKET_NAME=your-bucket-name

# Server Configuration
PORT=8000
EOF
    echo "⚠️  Please edit $BACKEND_DIR/.env and update:"
    echo "   - DATABASE_URL password"
    echo "   - AWS credentials (if using S3)"
    chown ubuntu:ubuntu "$BACKEND_DIR/.env"
else
    echo "✅ .env file already exists"
fi

# Create log directory
echo "📋 Step 11: Creating log directory..."
mkdir -p "$LOG_DIR"
chown ubuntu:ubuntu "$LOG_DIR"
chmod 755 "$LOG_DIR"

# Create uploads directory
echo "📁 Step 12: Setting up uploads directory..."
mkdir -p "$BACKEND_DIR/uploads"
chown ubuntu:ubuntu "$BACKEND_DIR/uploads"
chmod 755 "$BACKEND_DIR/uploads"

# Initialize database
echo "💾 Step 13: Initializing database..."
cd "$BACKEND_DIR"
source venv/bin/activate
python init_db.py

# Setup systemd service
echo "⚙️ Step 14: Setting up systemd service..."
if [ -f "$APP_DIR/sequoalpha.service" ]; then
    cp "$APP_DIR/sequoalpha.service" /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable sequoalpha
    systemctl start sequoalpha
    echo "✅ Systemd service configured and started"
else
    echo "⚠️  sequoalpha.service file not found, skipping systemd setup"
fi

# Setup Nginx
echo "🌐 Step 15: Setting up Nginx..."
if [ -f "$APP_DIR/nginx.conf" ]; then
    cp "$APP_DIR/nginx.conf" /etc/nginx/sites-available/sequoalpha
    
    # Remove default site
    rm -f /etc/nginx/sites-enabled/default
    
    # Enable our site
    ln -sf /etc/nginx/sites-available/sequoalpha /etc/nginx/sites-enabled/
    
    # Test nginx configuration
    nginx -t
    
    # Restart nginx
    systemctl restart nginx
    systemctl enable nginx
    echo "✅ Nginx configured and started"
else
    echo "⚠️  nginx.conf file not found, skipping Nginx setup"
fi

# Setup firewall
echo "🔒 Step 16: Setting up firewall..."
ufw --force enable
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw status
echo "✅ Firewall configured"

# Fix permissions
echo "🔧 Step 17: Fixing permissions..."
chown -R ubuntu:ubuntu "$APP_DIR"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit $BACKEND_DIR/.env with your actual credentials"
echo "2. Update /etc/nginx/sites-available/sequoalpha with your domain/IP"
echo "3. Restart services:"
echo "   sudo systemctl restart sequoalpha"
echo "   sudo systemctl restart nginx"
echo ""
echo "📊 Check status:"
echo "   sudo systemctl status sequoalpha"
echo "   sudo systemctl status nginx"
echo ""
echo "📋 View logs:"
echo "   sudo journalctl -u sequoalpha -f"
echo "   sudo tail -f /var/log/nginx/error.log"
echo ""
echo "🌍 Access your application:"
echo "   http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo ""
echo "🔐 Default credentials:"
echo "   Admin: admin / admin123"
echo "   User: user / user123"
echo ""
echo "⚠️  IMPORTANT: Change default passwords immediately!"
echo ""

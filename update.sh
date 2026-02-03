#!/bin/bash

# Quick Update/Redeploy Script for SequoAlpha on EC2
# Run this script whenever you push updates to your repository
# Usage: ./update.sh

set -e

echo "🔄 SequoAlpha Update Script"
echo "==========================="
echo ""

APP_DIR="/home/ubuntu/sequoalpha"
BACKEND_DIR="$APP_DIR/backend"

# Check if running as ubuntu user
if [ "$USER" != "ubuntu" ]; then
    echo "⚠️  This script should be run as ubuntu user"
    echo "   Switching to ubuntu..."
    exec sudo -u ubuntu bash "$0" "$@"
fi

cd "$APP_DIR"

echo "📥 Step 1: Pulling latest changes from repository..."
git pull origin main || git pull origin master

echo "🐍 Step 2: Updating Python dependencies..."
cd "$BACKEND_DIR"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "💾 Step 3: Running database migrations (if any)..."
python init_db.py

echo "🔄 Step 4: Restarting backend service..."
sudo systemctl restart sequoalpha

echo "⏳ Waiting for service to start..."
sleep 3

echo "📊 Step 5: Checking service status..."
sudo systemctl status sequoalpha --no-pager -l

echo "🌐 Step 6: Restarting Nginx..."
sudo systemctl restart nginx

echo ""
echo "✅ Update complete!"
echo ""
echo "📋 View logs:"
echo "   sudo journalctl -u sequoalpha -f"
echo ""
echo "🔍 Check status:"
echo "   sudo systemctl status sequoalpha"
echo ""

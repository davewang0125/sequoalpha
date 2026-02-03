#!/bin/bash

# SSL Certificate Setup Script for SequoAlpha
# This script automates SSL certificate generation using Let's Encrypt
# Usage: sudo ./setup-ssl.sh yourdomain.com

set -e

echo "🔒 SequoAlpha SSL Certificate Setup"
echo "===================================="
echo ""

# Check if running as root/sudo
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root or with sudo"
    exit 1
fi

# Check if domain argument is provided
if [ -z "$1" ]; then
    echo "❌ Please provide your domain name"
    echo ""
    echo "Usage: sudo ./setup-ssl.sh yourdomain.com"
    echo ""
    echo "Example:"
    echo "  sudo ./setup-ssl.sh sequoalpha.com"
    echo ""
    exit 1
fi

DOMAIN=$1
WWW_DOMAIN="www.$DOMAIN"

echo "📋 Configuration:"
echo "   Domain: $DOMAIN"
echo "   WWW Domain: $WWW_DOMAIN"
echo ""

# Check if domain resolves to this server
echo "🔍 Step 1: Checking DNS configuration..."
SERVER_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
DOMAIN_IP=$(dig +short $DOMAIN | tail -n1)

echo "   Server IP: $SERVER_IP"
echo "   Domain IP: $DOMAIN_IP"

if [ "$SERVER_IP" != "$DOMAIN_IP" ]; then
    echo ""
    echo "⚠️  WARNING: Domain does not point to this server!"
    echo "   Expected: $SERVER_IP"
    echo "   Found: $DOMAIN_IP"
    echo ""
    echo "Please update your DNS records:"
    echo "  1. Go to your domain registrar"
    echo "  2. Add A record: @ → $SERVER_IP"
    echo "  3. Add A record: www → $SERVER_IP"
    echo "  4. Wait 5-30 minutes for DNS propagation"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if Nginx is running
echo ""
echo "🌐 Step 2: Checking Nginx..."
if ! systemctl is-active --quiet nginx; then
    echo "❌ Nginx is not running"
    echo "   Starting Nginx..."
    systemctl start nginx
fi
echo "✅ Nginx is running"

# Update Nginx configuration with domain
echo ""
echo "📝 Step 3: Updating Nginx configuration..."
NGINX_CONFIG="/etc/nginx/sites-available/sequoalpha"

if [ ! -f "$NGINX_CONFIG" ]; then
    echo "❌ Nginx configuration not found: $NGINX_CONFIG"
    echo "   Please run the deployment script first: sudo ./deploy_ec2.sh"
    exit 1
fi

# Backup current config
cp $NGINX_CONFIG ${NGINX_CONFIG}.backup

# Update server_name in Nginx config
sed -i "s/server_name .*/server_name $DOMAIN $WWW_DOMAIN;/" $NGINX_CONFIG

# Test Nginx configuration
if nginx -t 2>&1 | grep -q "successful"; then
    echo "✅ Nginx configuration updated"
    systemctl reload nginx
else
    echo "❌ Nginx configuration error"
    echo "   Restoring backup..."
    mv ${NGINX_CONFIG}.backup $NGINX_CONFIG
    systemctl reload nginx
    exit 1
fi

# Install Certbot if not already installed
echo ""
echo "📦 Step 4: Installing Certbot..."
if ! command -v certbot &> /dev/null; then
    apt update
    apt install -y certbot python3-certbot-nginx
    echo "✅ Certbot installed"
else
    echo "✅ Certbot already installed"
fi

# Generate SSL certificate
echo ""
echo "🎯 Step 5: Generating SSL certificate..."
echo ""
echo "⚠️  You will be asked to:"
echo "   1. Enter your email address"
echo "   2. Agree to Terms of Service"
echo "   3. Choose to redirect HTTP to HTTPS (recommended: Yes)"
echo ""
read -p "Press Enter to continue..."

# Run certbot
certbot --nginx -d $DOMAIN -d $WWW_DOMAIN

# Check if certificate was generated
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo ""
    echo "✅ SSL certificate generated successfully!"
    echo ""
    echo "📋 Certificate details:"
    certbot certificates | grep -A 10 $DOMAIN
else
    echo ""
    echo "❌ Certificate generation failed"
    echo "   Check the errors above and try again"
    exit 1
fi

# Setup auto-renewal hook
echo ""
echo "🔄 Step 6: Setting up auto-renewal..."
mkdir -p /etc/letsencrypt/renewal-hooks/deploy

cat > /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh <<EOF
#!/bin/bash
systemctl reload nginx
echo "\$(date): Nginx reloaded after certificate renewal" >> /var/log/sequoalpha/ssl-renewal.log
EOF

chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh
echo "✅ Auto-renewal configured"

# Test renewal
echo ""
echo "🧪 Step 7: Testing auto-renewal..."
if certbot renew --dry-run 2>&1 | grep -q "Congratulations"; then
    echo "✅ Auto-renewal test passed"
else
    echo "⚠️  Auto-renewal test failed (check manually later)"
fi

# Final checks
echo ""
echo "🔍 Step 8: Running final checks..."

# Check HTTPS
if curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN | grep -q "200"; then
    echo "✅ HTTPS is working"
else
    echo "⚠️  HTTPS check failed (might take a moment)"
fi

# Print summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 SSL Certificate Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Your site is now secured with HTTPS"
echo ""
echo "📋 Certificate Information:"
echo "   Domain: $DOMAIN, $WWW_DOMAIN"
echo "   Certificate: /etc/letsencrypt/live/$DOMAIN/fullchain.pem"
echo "   Private Key: /etc/letsencrypt/live/$DOMAIN/privkey.pem"
echo "   Expires: 90 days (auto-renewal enabled)"
echo ""
echo "🌐 Access your site:"
echo "   https://$DOMAIN"
echo "   https://$WWW_DOMAIN"
echo ""
echo "🔄 Auto-renewal:"
echo "   Certificates will automatically renew"
echo "   Check status: sudo certbot renew --dry-run"
echo ""
echo "📊 Test SSL security:"
echo "   https://www.ssllabs.com/ssltest/analyze.html?d=$DOMAIN"
echo ""
echo "⚠️  Remember to:"
echo "   1. Change default application passwords"
echo "   2. Update any hardcoded HTTP URLs to HTTPS"
echo "   3. Test all functionality (login, uploads, downloads)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

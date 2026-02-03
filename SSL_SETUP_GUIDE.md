# 🔒 SSL Certificate Setup Guide (HTTPS)

This guide shows you how to generate FREE SSL certificates using Let's Encrypt for your SequoAlpha deployment.

## 📋 Prerequisites

Before starting, ensure:
- [ ] Your EC2 instance is running and accessible
- [ ] Your domain name is pointed to your EC2 IP address
- [ ] Nginx is installed and running
- [ ] Ports 80 and 443 are open in your Security Group

## 🌍 Step 1: Point Your Domain to EC2

### 1.1 Get Your EC2 Public IP
```bash
# On your EC2 instance
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

### 1.2 Update DNS Records
Go to your domain registrar (GoDaddy, Namecheap, Route53, etc.) and add:

**A Records:**
- **Host**: `@` (root domain) → **Value**: Your EC2 IP
- **Host**: `www` → **Value**: Your EC2 IP

**Example:**
```
Type    Host    Value           TTL
A       @       54.123.45.67    600
A       www     54.123.45.67    600
```

### 1.3 Verify DNS Propagation
```bash
# Check if DNS is working (run from your local machine)
nslookup sequoalpha.com
ping sequoalpha.com

# Should return your EC2 IP address
```

⏰ **Wait 5-30 minutes for DNS to propagate** before proceeding.

## 🔧 Step 2: Update Nginx Configuration

Before installing the certificate, update your Nginx config with your domain:

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Edit Nginx configuration
sudo nano /etc/nginx/sites-available/sequoalpha
```

**Update the server_name line:**
```nginx
server {
    listen 80;
    server_name sequoalpha.com www.sequoalpha.com;  # Replace with YOUR domain

    # ... rest of configuration stays the same
}
```

**Test and reload Nginx:**
```bash
# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

**Verify HTTP is working:**
```bash
# From your local machine or browser
curl http://sequoalpha.com
# Should show your website
```

## 🚀 Step 3: Install Certbot

Certbot is the official Let's Encrypt client that automates certificate generation.

```bash
# Update package list
sudo apt update

# Install certbot and nginx plugin
sudo apt install -y certbot python3-certbot-nginx
```

## 🎯 Step 4: Generate SSL Certificate

### Option A: Automatic Configuration (Recommended)

Certbot will automatically configure Nginx for you:

```bash
# Generate certificate and auto-configure Nginx
sudo certbot --nginx -d sequoalpha.com -d www.sequoalpha.com
```

**Follow the prompts:**
1. **Email**: Enter your email (for renewal notifications)
2. **Terms**: Agree to terms of service (Yes)
3. **Share email**: Optional (your choice)
4. **Redirect HTTP to HTTPS**: Choose option 2 (Redirect)

### Option B: Certificate Only (Manual Configuration)

If you want to manually configure Nginx:

```bash
# Generate certificate only
sudo certbot certonly --nginx -d sequoalpha.com -d www.sequoalpha.com
```

Then manually update your Nginx configuration (see Step 5).

## ✅ Step 5: Verify Installation

### 5.1 Check Certificate Files
```bash
# List certificate files
sudo ls -la /etc/letsencrypt/live/sequoalpha.com/

# You should see:
# - fullchain.pem (your certificate + chain)
# - privkey.pem (your private key)
# - cert.pem (your certificate only)
# - chain.pem (intermediate certificates)
```

### 5.2 Test HTTPS
```bash
# From your local machine
curl https://sequoalpha.com

# Or open in browser
# https://sequoalpha.com
```

### 5.3 Check SSL Grade
Visit: https://www.ssllabs.com/ssltest/
- Enter your domain
- Should get A or A+ rating

## 🔧 Step 6: Manual Nginx Configuration (If Needed)

If you used "certonly" or want to customize, update your Nginx config:

```bash
sudo nano /etc/nginx/sites-available/sequoalpha
```

**Replace entire file with:**
```nginx
# HTTP - Redirect to HTTPS
server {
    listen 80;
    server_name sequoalpha.com www.sequoalpha.com;

    # Redirect all HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS - Main Configuration
server {
    listen 443 ssl http2;
    server_name sequoalpha.com www.sequoalpha.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/sequoalpha.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sequoalpha.com/privkey.pem;

    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/sequoalpha.com/chain.pem;

    # Maximum file upload size
    client_max_body_size 50M;

    # Root directory for frontend static files
    root /home/ubuntu/sequoalpha;
    index index.html;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;

    # Backend API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for large file uploads
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }

    # Direct backend endpoints (without /api prefix)
    location ~ ^/(login|users|admin|documents|debug|test-cors) {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for large file uploads
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }

    # Serve static frontend files
    location / {
        try_files $uri $uri/ /index.html;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # CSS files
    location /css/ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # JavaScript files
    location /frontend/js/ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Images
    location /images/ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Deny access to backend files
    location ~ ^/backend/ {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Logging
    access_log /var/log/nginx/sequoalpha_access.log;
    error_log /var/log/nginx/sequoalpha_error.log;
}
```

**Test and reload:**
```bash
# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

## 🔄 Step 7: Auto-Renewal Setup

Let's Encrypt certificates expire after 90 days. Certbot automatically sets up renewal.

### 7.1 Test Auto-Renewal
```bash
# Test renewal process (doesn't actually renew)
sudo certbot renew --dry-run
```

### 7.2 Check Renewal Timer
```bash
# Check if renewal timer is active
sudo systemctl status certbot.timer

# Should show "active (waiting)"
```

### 7.3 Manual Renewal (if needed)
```bash
# Manually renew certificates
sudo certbot renew

# Reload Nginx after renewal
sudo systemctl reload nginx
```

### 7.4 Auto-Reload Nginx After Renewal

Create a renewal hook:
```bash
# Create hook script
sudo nano /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh
```

**Add this content:**
```bash
#!/bin/bash
systemctl reload nginx
```

**Make it executable:**
```bash
sudo chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh
```

Now Nginx will automatically reload when certificates are renewed.

## 🐛 Troubleshooting

### Certificate Generation Failed

**Error: "Domain validation failed"**
```bash
# Check if domain points to your server
nslookup sequoalpha.com

# Check if port 80 is accessible
curl http://sequoalpha.com

# Check Nginx is running
sudo systemctl status nginx

# Check firewall
sudo ufw status
```

**Error: "Too many failed authorizations"**
- Let's Encrypt has rate limits
- Wait 1 hour and try again
- Use staging environment for testing:
  ```bash
  sudo certbot --nginx --staging -d sequoalpha.com -d www.sequoalpha.com
  ```

### Certificate Files Not Found

```bash
# List all certificates
sudo certbot certificates

# Check directory
sudo ls -la /etc/letsencrypt/live/

# Regenerate if needed
sudo certbot --nginx -d sequoalpha.com -d www.sequoalpha.com --force-renewal
```

### Mixed Content Errors

If you see "mixed content" errors in browser:
1. Update frontend config to use HTTPS
2. Check for hardcoded HTTP URLs in your code
3. Ensure all API calls use relative URLs or HTTPS

### Permission Errors

```bash
# Fix certificate permissions
sudo chmod 0755 /etc/letsencrypt/live
sudo chmod 0755 /etc/letsencrypt/archive
```

## 🧪 Testing Checklist

After SSL setup, verify:
- [ ] https://sequoalpha.com loads correctly
- [ ] https://www.sequoalpha.com loads correctly
- [ ] http://sequoalpha.com redirects to HTTPS
- [ ] Browser shows green padlock icon
- [ ] Can login to application
- [ ] Can upload/download documents
- [ ] No mixed content warnings
- [ ] SSL Labs gives A or A+ rating

## 📋 Certificate Information

### View Certificate Details
```bash
# View certificate info
sudo certbot certificates

# Output shows:
# - Certificate Name
# - Domains
# - Expiry Date
# - Certificate Path
# - Private Key Path
```

### Certificate File Locations
```
/etc/letsencrypt/
├── live/sequoalpha.com/
│   ├── fullchain.pem    → Use in nginx (ssl_certificate)
│   ├── privkey.pem      → Use in nginx (ssl_certificate_key)
│   ├── cert.pem         → Your certificate only
│   └── chain.pem        → Intermediate certificates
├── archive/             → Actual certificate files
└── renewal/             → Renewal configuration
```

## 🔐 Security Best Practices

1. **Keep Certificates Private**
   - Never share or commit `privkey.pem`
   - Restrict permissions to root only

2. **Monitor Expiration**
   - Certificates expire in 90 days
   - Auto-renewal runs twice daily
   - Setup monitoring/alerts

3. **Use Strong Ciphers**
   - Configuration above uses modern ciphers
   - Disables old TLS 1.0/1.1

4. **Enable HSTS**
   - Already included in config
   - Forces browsers to use HTTPS

5. **Regular Testing**
   - Test SSL Labs quarterly
   - Monitor renewal logs

## 📞 Support Resources

### Certbot Documentation
- Official Docs: https://certbot.eff.org/
- Let's Encrypt: https://letsencrypt.org/

### Useful Commands
```bash
# List all certificates
sudo certbot certificates

# Renew specific certificate
sudo certbot renew --cert-name sequoalpha.com

# Delete certificate
sudo certbot delete --cert-name sequoalpha.com

# Expand certificate (add domains)
sudo certbot --nginx -d sequoalpha.com -d www.sequoalpha.com -d api.sequoalpha.com --expand
```

## 🎉 Success!

Your site is now secured with HTTPS! 🔒

**Your certificate includes:**
- ✅ Free SSL/TLS certificate from Let's Encrypt
- ✅ Valid for 90 days with auto-renewal
- ✅ Covers sequoalpha.com and www.sequoalpha.com
- ✅ A/A+ grade security

**Next Steps:**
1. Update any external links to use HTTPS
2. Update API documentation with HTTPS URLs
3. Setup monitoring for certificate expiration
4. Consider adding more subdomains if needed

---

© 2025 SequoAlpha Management LP. All rights reserved.

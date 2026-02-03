# Migration from Render/Netlify to EC2 - Changes Summary

## 📝 What Has Changed

### ✅ New Files Created

1. **EC2_DEPLOYMENT.md** - Comprehensive deployment guide for EC2
2. **QUICKSTART_EC2.md** - Quick reference guide
3. **nginx.conf** - Nginx configuration for reverse proxy and static file serving
4. **sequoalpha.service** - Systemd service configuration
5. **deploy_ec2.sh** - Automated deployment script
6. **update.sh** - Quick update/redeploy script
7. **backend/.env.example** - Environment variable template

### 🔧 Modified Files

1. **frontend/js/config.js** - Updated to support EC2 deployment with relative API paths

### 🗑️ Files You Can Remove (Optional)

These files are specific to Render/Netlify and are no longer needed for EC2:

1. **render.yaml** - Render-specific configuration
2. **netlify.toml** - Netlify-specific configuration
3. **RENDER_DEPLOYMENT.md** - Render deployment instructions
4. **backend/start.sh** - Render-specific startup script (replaced by systemd)
5. **_redirects** - Netlify redirects (handled by nginx now)

## 🚀 Deployment Architecture Comparison

### Old (Render/Netlify)
```
Frontend (Netlify) → Backend (Render) → PostgreSQL (Render)
                            ↓
                        AWS S3 (Optional)
```

### New (EC2)
```
Internet → EC2 Instance
          ├── Nginx (Port 80/443)
          │   ├── Serves Frontend (/)
          │   └── Proxies to Backend (/api)
          ├── Gunicorn/Flask (Port 8000)
          ├── PostgreSQL (Local or RDS)
          └── AWS S3 (File Storage)
```

## 🔑 Key Changes Explained

### 1. Frontend Hosting
- **Before**: Netlify CDN
- **After**: Nginx serves static files from `/home/ubuntu/sequoalpha/`
- **Why**: Single server reduces complexity and costs

### 2. API Endpoint
- **Before**: `https://sequoalpha-backend.onrender.com`
- **After**: `/api` (relative path, proxied by nginx)
- **Why**: Same origin, no CORS issues, simpler configuration

### 3. Backend Server
- **Before**: Render managed service with `start.sh`
- **After**: Systemd service with Gunicorn
- **Why**: Full control, better performance, persistent process

### 4. Database
- **Before**: Render PostgreSQL (managed)
- **After**: Local PostgreSQL or RDS (your choice)
- **Why**: Cost control and flexibility

### 5. File Storage
- **Before**: Ephemeral local storage (files lost on restart)
- **After**: AWS S3 with local fallback
- **Why**: Persistence and reliability

## 📋 What You Need to Do

### Pre-Deployment Checklist

- [ ] Launch EC2 instance (Ubuntu 22.04, t2.small+)
- [ ] Configure Security Group (ports 22, 80, 443)
- [ ] Create AWS S3 bucket (optional but recommended)
- [ ] Get AWS IAM credentials for S3
- [ ] Purchase/configure domain name (optional)

### Deployment Steps

1. **Connect to EC2**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. **Clone repository**:
   ```bash
   cd /home/ubuntu
   git clone https://github.com/yourusername/sequoalpha.git
   cd sequoalpha
   ```

3. **Run deployment script**:
   ```bash
   chmod +x deploy_ec2.sh
   sudo ./deploy_ec2.sh
   ```

4. **Configure environment**:
   ```bash
   cd backend
   cp .env.example .env
   nano .env
   # Update all values marked with "changeme" or "your-"
   ```

5. **Update nginx config**:
   ```bash
   sudo nano /etc/nginx/sites-available/sequoalpha
   # Replace 'your-domain.com' with your actual domain or EC2 public IP
   ```

6. **Restart services**:
   ```bash
   sudo systemctl restart sequoalpha
   sudo systemctl restart nginx
   ```

7. **Verify deployment**:
   ```bash
   # Check backend
   sudo systemctl status sequoalpha
   
   # Check nginx
   sudo systemctl status nginx
   
   # Test API
   curl http://localhost:8000/
   
   # Visit in browser
   # http://your-ec2-ip
   ```

### Post-Deployment (Recommended)

- [ ] Setup SSL/HTTPS with Let's Encrypt
- [ ] Configure automatic backups
- [ ] Setup monitoring (CloudWatch)
- [ ] Configure Route 53 for domain
- [ ] Change default admin password
- [ ] Setup log rotation
- [ ] Configure auto-scaling (if needed)

## 💰 Cost Comparison

### Render/Netlify (Current)
- Netlify: Free tier (limited builds)
- Render: $7-21/month (free tier sleeps)
- Render PostgreSQL: $7/month (free tier limited)
- **Total**: ~$14-28/month + limitations

### EC2 (New)
- EC2 t2.small: ~$17/month (24/7)
- EC2 t2.medium: ~$34/month (24/7)
- PostgreSQL: Included (local) or $15/month (RDS)
- S3: ~$0.023/GB/month
- Data Transfer: ~$0.09/GB
- **Total**: ~$20-50/month + full control

## 🎯 Benefits of EC2

1. **Full Control**: Root access, custom configurations
2. **No Sleep**: Always on, no cold starts
3. **Better Performance**: Dedicated resources
4. **Flexibility**: Install any software you need
5. **Cost Predictable**: Fixed monthly cost
6. **Scalability**: Easy to upgrade instance size
7. **Integration**: Easy AWS service integration

## ⚠️ Important Notes

### Environment Variables
Make sure to set all required variables in `backend/.env`:
- `SECRET_KEY` - Generate new one: `python3 -c 'import secrets; print(secrets.token_urlsafe(32))'`
- `DATABASE_URL` - Update with secure password
- AWS credentials - If using S3

### Security
- Change default passwords immediately
- Setup firewall (ufw)
- Configure SSL certificates
- Restrict SSH access
- Regular security updates

### Backup Strategy
- Database: Daily pg_dump
- Files: S3 provides durability
- Config: Keep .env backed up securely
- Code: Git repository

## 📞 Troubleshooting

### Backend not starting
```bash
sudo journalctl -u sequoalpha -n 100
sudo systemctl status sequoalpha
```

### Nginx errors
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

### Database connection issues
```bash
sudo systemctl status postgresql
sudo -u postgres psql sequoalpha
```

### Can't access from browser
- Check Security Group allows port 80
- Check nginx is running: `sudo systemctl status nginx`
- Check firewall: `sudo ufw status`

## 📚 Additional Resources

- Full deployment guide: `EC2_DEPLOYMENT.md`
- Quick reference: `QUICKSTART_EC2.md`
- AWS S3 setup: `AWS_S3_SETUP.md`
- Environment template: `backend/.env.example`

## 🎉 Next Steps After Successful Deployment

1. Test all functionality
2. Setup SSL with Let's Encrypt
3. Configure domain name
4. Setup monitoring and alerts
5. Create backup scripts
6. Document your specific configuration
7. Setup CI/CD (optional)

---

**Need Help?** Check the logs and refer to EC2_DEPLOYMENT.md for detailed instructions.

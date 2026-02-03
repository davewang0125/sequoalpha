# EC2 Deployment Checklist

Use this checklist to track your deployment progress. Mark items with ✅ as you complete them.

## 📋 Pre-Deployment

### AWS Account Setup
- [ ] AWS account created
- [ ] Payment method configured
- [ ] Understand EC2 pricing (~$20-50/month)
- [ ] (Optional) Domain name purchased

### Local Preparation
- [ ] Read EC2_DEPLOYMENT.md
- [ ] Read MIGRATION_GUIDE.md
- [ ] Review ARCHITECTURE_DIAGRAM.txt
- [ ] Git repository ready to clone

### AWS S3 Setup (Recommended)
- [ ] S3 bucket created (follow AWS_S3_SETUP.md)
- [ ] IAM user created with S3 access
- [ ] Access Key ID saved
- [ ] Secret Access Key saved
- [ ] Bucket name noted

---

## 🖥️ EC2 Instance Setup

### Launch Instance
- [ ] Logged into AWS Console
- [ ] Navigated to EC2 Dashboard
- [ ] Clicked "Launch Instance"
- [ ] Selected Ubuntu Server 22.04 LTS
- [ ] Chosen instance type: t2.small or t2.medium
- [ ] Created or selected key pair (.pem file)
- [ ] Downloaded and saved .pem file securely

### Security Group Configuration
- [ ] Created/configured Security Group
- [ ] Added rule: SSH (22) - My IP
- [ ] Added rule: HTTP (80) - Anywhere (0.0.0.0/0)
- [ ] Added rule: HTTPS (443) - Anywhere (0.0.0.0/0)
- [ ] (Optional) Custom TCP (8000) - Anywhere (for testing only)
- [ ] Instance launched successfully
- [ ] Noted Public IP address: ___________________

### Initial Connection
- [ ] Changed .pem file permissions: `chmod 400 your-key.pem`
- [ ] Connected via SSH: `ssh -i your-key.pem ubuntu@your-ec2-ip`
- [ ] Connection successful

---

## 🚀 Deployment Process

### Clone Repository
- [ ] Navigated to /home/ubuntu
- [ ] Cloned repository: `git clone <your-repo>`
- [ ] Changed into project directory
- [ ] Verified all files present

### Run Deployment Script
- [ ] Made script executable: `chmod +x deploy_ec2.sh`
- [ ] Ran deployment: `sudo ./deploy_ec2.sh`
- [ ] Script completed without errors
- [ ] Noted any warnings or messages

### Database Setup
- [ ] PostgreSQL installed
- [ ] Database 'sequoalpha' created
- [ ] User 'sequoalpha_user' created
- [ ] Database initialized successfully
- [ ] Test data loaded

---

## ⚙️ Configuration

### Environment Variables (.env)
- [ ] Copied template: `cp backend/.env.example backend/.env`
- [ ] Opened for editing: `nano backend/.env`
- [ ] Generated new SECRET_KEY
- [ ] Updated DATABASE_URL password
- [ ] Added AWS_ACCESS_KEY_ID (if using S3)
- [ ] Added AWS_SECRET_ACCESS_KEY (if using S3)
- [ ] Added AWS_REGION (if using S3)
- [ ] Added AWS_S3_BUCKET_NAME (if using S3)
- [ ] Saved and closed file

### Nginx Configuration
- [ ] Opened config: `sudo nano /etc/nginx/sites-available/sequoalpha`
- [ ] Replaced 'your-domain.com' with actual domain or EC2 IP
- [ ] Saved and closed file
- [ ] Tested config: `sudo nginx -t`
- [ ] Config test passed

### Service Configuration
- [ ] Systemd service file in place
- [ ] Service enabled: `sudo systemctl enable sequoalpha`
- [ ] Nginx enabled: `sudo systemctl enable nginx`

---

## 🔄 Start Services

### Backend Service
- [ ] Started backend: `sudo systemctl start sequoalpha`
- [ ] Checked status: `sudo systemctl status sequoalpha`
- [ ] Service is active and running
- [ ] No errors in status output

### Nginx Service
- [ ] Restarted Nginx: `sudo systemctl restart nginx`
- [ ] Checked status: `sudo systemctl status nginx`
- [ ] Nginx is active and running
- [ ] No errors in status output

---

## 🧪 Testing

### Backend API Tests
- [ ] Test root: `curl http://localhost:8000/`
- [ ] Received JSON response
- [ ] Test CORS: `curl http://localhost:8000/test-cors`
- [ ] CORS working

### Frontend Tests
- [ ] Accessed in browser: `http://your-ec2-ip`
- [ ] Homepage loads correctly
- [ ] CSS styles applied
- [ ] JavaScript console shows correct API URL
- [ ] No 404 errors for static files

### Authentication Tests
- [ ] Clicked Login
- [ ] Logged in as admin (admin/admin123)
- [ ] Dashboard loaded successfully
- [ ] Can navigate between pages

### Document Management Tests
- [ ] Uploaded a test document
- [ ] Document appears in list
- [ ] Can download document
- [ ] Document opens correctly

### User Management Tests (Admin)
- [ ] Created a test user
- [ ] User appears in users list
- [ ] Logged out
- [ ] Logged in as test user
- [ ] User dashboard loads
- [ ] User can view documents

---

## 🔒 Security Hardening

### Immediate Security
- [ ] Changed admin password from default
- [ ] Changed test user password
- [ ] Verified SECRET_KEY is unique
- [ ] Database password is strong
- [ ] .env file permissions: `chmod 600 backend/.env`

### Firewall Setup
- [ ] UFW enabled: `sudo ufw enable`
- [ ] SSH allowed: `sudo ufw allow OpenSSH`
- [ ] Nginx allowed: `sudo ufw allow 'Nginx Full'`
- [ ] Firewall status checked: `sudo ufw status`

### SSH Security
- [ ] Security Group restricts SSH to my IP
- [ ] Removed test port 8000 from Security Group
- [ ] (Optional) Disabled password authentication
- [ ] (Optional) Setup SSH key rotation plan

---

## 🔐 SSL/HTTPS Setup (Recommended)

### Domain Configuration (If using domain)
- [ ] Domain DNS pointed to EC2 IP
- [ ] DNS propagation verified
- [ ] Can access site via domain name

### Let's Encrypt SSL
- [ ] Installed certbot: `sudo apt install certbot python3-certbot-nginx`
- [ ] Ran certbot: `sudo certbot --nginx -d yourdomain.com`
- [ ] Certificate obtained successfully
- [ ] HTTPS redirect configured
- [ ] Tested HTTPS: `https://yourdomain.com`
- [ ] SSL certificate auto-renewal tested: `sudo certbot renew --dry-run`

### SSL Without Domain (Self-signed)
- [ ] Generated self-signed certificate
- [ ] Nginx configured for SSL
- [ ] HTTPS accessible (with browser warning)

---

## 📊 Monitoring Setup

### Log Verification
- [ ] Backend logs accessible: `sudo journalctl -u sequoalpha -n 50`
- [ ] Nginx access logs: `sudo tail -f /var/log/nginx/sequoalpha_access.log`
- [ ] Nginx error logs: `sudo tail -f /var/log/nginx/sequoalpha_error.log`
- [ ] No critical errors in logs

### Management Scripts
- [ ] Tested `./manage.sh status`
- [ ] Tested `./manage.sh logs`
- [ ] Tested `./manage.sh test`
- [ ] Tested `./manage.sh errors`
- [ ] All scripts working correctly

### Health Checks
- [ ] Setup monitoring script (optional)
- [ ] Configure CloudWatch (optional)
- [ ] Setup email alerts (optional)

---

## 💾 Backup Configuration

### Database Backups
- [ ] Tested manual backup: `./manage.sh backup`
- [ ] Backup file created successfully
- [ ] Can restore from backup
- [ ] (Optional) Setup automated daily backups

### File Backups
- [ ] S3 configured (files auto-backed up)
- [ ] OR manual file backup strategy in place
- [ ] .env file backed up securely
- [ ] nginx.conf backed up

### Disaster Recovery Plan
- [ ] Documented restore procedure
- [ ] Backup restoration tested
- [ ] Recovery time estimated
- [ ] Backup storage location secure

---

## 📈 Performance Optimization

### Server Resources
- [ ] Checked CPU usage: `top`
- [ ] Checked memory usage: `free -h`
- [ ] Checked disk space: `df -h`
- [ ] All resources within acceptable limits

### Application Performance
- [ ] Page load times acceptable (<3 seconds)
- [ ] API response times fast (<500ms)
- [ ] File uploads working smoothly
- [ ] No timeout errors

### Optimization (Optional)
- [ ] Gunicorn worker count optimized
- [ ] Nginx caching configured
- [ ] Database indexes reviewed
- [ ] S3 CDN considered

---

## 🔄 Update Deployment

### Update Process
- [ ] Made test code change locally
- [ ] Pushed to GitHub
- [ ] Ran `./update.sh` on EC2
- [ ] Update completed successfully
- [ ] Changes visible in application
- [ ] No errors after update

### Rollback Plan
- [ ] Documented rollback procedure
- [ ] Know how to revert to previous version
- [ ] Database migration rollback understood

---

## 📝 Documentation

### Internal Documentation
- [ ] Documented server IP address
- [ ] Documented SSH key location
- [ ] Documented database credentials
- [ ] Documented AWS credentials
- [ ] Documented admin credentials
- [ ] Created runbook for common tasks

### Team Knowledge
- [ ] Shared access credentials securely
- [ ] Trained team on ./manage.sh usage
- [ ] Shared ./update.sh procedure
- [ ] Emergency contact plan established

---

## ✅ Final Verification

### Functionality Check
- [ ] All pages load without errors
- [ ] Login/logout works
- [ ] Document upload works
- [ ] Document download works
- [ ] User creation works (admin)
- [ ] User login works
- [ ] All API endpoints respond

### Production Readiness
- [ ] Default passwords changed
- [ ] Security Group properly configured
- [ ] Firewall enabled and configured
- [ ] SSL/HTTPS working (or planned)
- [ ] Backups configured
- [ ] Monitoring in place
- [ ] Update procedure tested
- [ ] Team trained

### Go-Live Decision
- [ ] All critical items completed
- [ ] All tests passed
- [ ] Stakeholders notified
- [ ] Support plan in place
- [ ] Ready for production traffic

---

## 🎉 Post-Deployment

### Communication
- [ ] Notified users of new URL
- [ ] Updated documentation with new URL
- [ ] Announced go-live

### Monitoring (First Week)
- [ ] Daily log review
- [ ] Daily backup verification
- [ ] Performance monitoring
- [ ] User feedback collected
- [ ] Issues logged and resolved

### Ongoing Maintenance
- [ ] Weekly backup verification
- [ ] Monthly security updates
- [ ] Quarterly SSL renewal check
- [ ] Regular cost monitoring

---

## 📞 Support Information

### Quick Reference
- **EC2 IP**: ___________________
- **Domain**: ___________________
- **SSH Key Location**: ___________________
- **Admin Email**: ___________________
- **Backup Location**: ___________________

### Emergency Contacts
- **AWS Support**: ___________________
- **Team Lead**: ___________________
- **DevOps**: ___________________

### Useful Commands
```bash
# Check status
./manage.sh status

# View logs
./manage.sh logs

# Restart services
./manage.sh restart

# Update app
./update.sh

# Backup database
./manage.sh backup
```

---

**Deployment Completion Date**: ___________________

**Deployed By**: ___________________

**Notes**: 
___________________
___________________
___________________

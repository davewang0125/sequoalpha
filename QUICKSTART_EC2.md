# EC2 Deployment Quick Reference

## 🚀 Quick Start

1. **Launch EC2 instance** (Ubuntu 22.04, t2.small or larger)
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
   nano backend/.env
   # Update database password, AWS credentials, etc.
   ```

5. **Update nginx configuration**:
   ```bash
   sudo nano /etc/nginx/sites-available/sequoalpha
   # Replace 'your-domain.com' with your actual domain or IP
   ```

6. **Restart services**:
   ```bash
   sudo systemctl restart sequoalpha
   sudo systemctl restart nginx
   ```

7. **Access your app**: `http://your-ec2-ip`

## 📋 Common Commands

### Service Management
```bash
# View backend logs
sudo journalctl -u sequoalpha -f

# Restart backend
sudo systemctl restart sequoalpha

# Check status
sudo systemctl status sequoalpha

# Restart nginx
sudo systemctl restart nginx
```

### Deployment Updates
```bash
# Quick update script
chmod +x update.sh
./update.sh

# Manual update
cd /home/ubuntu/sequoalpha
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart sequoalpha
```

### Database
```bash
# Access database
sudo -u postgres psql sequoalpha

# Backup database
pg_dump sequoalpha > backup_$(date +%Y%m%d).sql

# Restore database
psql sequoalpha < backup_file.sql
```

## 🔒 Security Checklist

- [ ] Change default admin password
- [ ] Update SECRET_KEY in .env
- [ ] Update database password
- [ ] Configure firewall (ufw)
- [ ] Setup SSL/HTTPS with certbot
- [ ] Restrict SSH access in Security Group
- [ ] Setup S3 for file storage
- [ ] Enable automated backups

## 📞 Support

See full documentation: [EC2_DEPLOYMENT.md](EC2_DEPLOYMENT.md)

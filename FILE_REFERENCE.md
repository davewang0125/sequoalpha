# 🎯 EC2 Deployment - File Reference Guide

## 📁 New Files Added for EC2 Deployment

### Documentation Files
| File | Purpose | When to Use |
|------|---------|-------------|
| `EC2_DEPLOYMENT.md` | Complete deployment guide | Read before deployment |
| `QUICKSTART_EC2.md` | Quick reference commands | Keep for daily operations |
| `MIGRATION_GUIDE.md` | Migration overview from Render/Netlify | Understand changes |
| `FILE_REFERENCE.md` | This file - quick navigation | Find files quickly |

### Configuration Files
| File | Purpose | Action Required |
|------|---------|-----------------|
| `nginx.conf` | Nginx web server config | ✅ Update domain/IP before use |
| `sequoalpha.service` | Systemd service config | ✅ Copy to `/etc/systemd/system/` |
| `backend/.env.example` | Environment template | ✅ Copy to `.env` and update |

### Automation Scripts
| File | Purpose | When to Run |
|------|---------|-------------|
| `deploy_ec2.sh` | Initial deployment | Once - first time setup |
| `update.sh` | Deploy updates | After git pull |
| `manage.sh` | Service management | Daily operations |

## 🔧 Modified Files

### Frontend Configuration
- `frontend/js/config.js` - Now supports EC2 with relative API paths

## 🗑️ Deprecated Files (Can be Removed)

These files were for Render/Netlify and are no longer needed:
- `render.yaml` - Render configuration
- `netlify.toml` - Netlify configuration  
- `RENDER_DEPLOYMENT.md` - Old deployment docs
- `backend/start.sh` - Render startup script
- `_redirects` - Netlify redirects

**Note**: Don't delete them yet until you've successfully deployed to EC2!

## 📋 Step-by-Step File Usage

### Phase 1: Preparation (Before EC2 Login)
1. Read `EC2_DEPLOYMENT.md` (entire document)
2. Read `MIGRATION_GUIDE.md` (understand changes)
3. Launch EC2 instance following security group setup in docs
4. Clone repository to EC2

### Phase 2: Initial Deployment (On EC2)
1. Run `deploy_ec2.sh` (automated setup)
2. Edit `backend/.env` (from `.env.example` template)
3. Edit `/etc/nginx/sites-available/sequoalpha` (nginx.conf location)
4. Restart services

### Phase 3: Testing
1. Use `manage.sh test` to verify
2. Use `manage.sh status` to check health
3. Use `manage.sh logs` to monitor

### Phase 4: Daily Operations
1. Use `update.sh` for updates
2. Use `manage.sh` for service control
3. Refer to `QUICKSTART_EC2.md` for commands

## 🎨 File Tree

```
sequoalpha/
├── 📚 Documentation
│   ├── EC2_DEPLOYMENT.md          ⭐ Main deployment guide
│   ├── QUICKSTART_EC2.md          ⭐ Quick reference
│   ├── MIGRATION_GUIDE.md         📖 Migration overview
│   ├── FILE_REFERENCE.md          📖 This file
│   ├── AWS_S3_SETUP.md            📖 S3 configuration
│   ├── README.md                  📖 Project overview
│   └── (deprecated)
│       ├── RENDER_DEPLOYMENT.md   🗑️ Old - can remove
│       └── render.yaml            🗑️ Old - can remove
│
├── ⚙️ Configuration Files
│   ├── nginx.conf                 ⭐ Nginx configuration
│   ├── sequoalpha.service         ⭐ Systemd service
│   ├── netlify.toml               🗑️ Old - can remove
│   └── _redirects                 🗑️ Old - can remove
│
├── 🔧 Scripts
│   ├── deploy_ec2.sh              ⭐ Initial deployment
│   ├── update.sh                  ⭐ Deploy updates
│   └── manage.sh                  ⭐ Service management
│
├── 🔙 Backend
│   ├── backend/
│   │   ├── main.py                🔧 Flask application
│   │   ├── models.py              🔧 Database models
│   │   ├── init_db.py             🔧 Database initialization
│   │   ├── s3_config.py           🔧 S3 file storage
│   │   ├── requirements.txt       📦 Python dependencies
│   │   ├── .env.example           ⭐ Environment template
│   │   ├── .env                   🔒 Your config (create this)
│   │   ├── start.sh               🗑️ Old - not needed
│   │   └── uploads/               📁 Local file storage
│
├── 🎨 Frontend
│   ├── index.html                 🌐 Main page
│   ├── frontend/js/
│   │   ├── config.js              ⭐ Updated for EC2
│   │   ├── App.js                 🌐 Main component
│   │   ├── Login.js               🌐 Login page
│   │   ├── Dashboard.js           🌐 Admin dashboard
│   │   ├── UserDashboard.js       🌐 User dashboard
│   │   └── DocumentCenter.js      🌐 Document management
│   ├── css/                       🎨 Stylesheets
│   └── images/                    🖼️ Images
│
└── 📋 Other
    └── .gitignore                 🔒 Git ignore rules
```

## ⭐ Most Important Files for EC2 Deployment

### Must Read
1. `EC2_DEPLOYMENT.md` - Complete instructions
2. `MIGRATION_GUIDE.md` - What changed and why

### Must Configure
1. `backend/.env` - Copy from `.env.example` and update
2. `nginx.conf` - Update domain/IP before copying to server

### Must Run
1. `deploy_ec2.sh` - First time deployment
2. `manage.sh` - Daily service management

## 🚀 Quick Command Reference

### First Time Setup
```bash
# On EC2 instance
git clone <your-repo>
cd sequoalpha
sudo ./deploy_ec2.sh
nano backend/.env              # Configure
sudo nano /etc/nginx/sites-available/sequoalpha  # Update domain
sudo systemctl restart sequoalpha nginx
```

### Daily Operations
```bash
./manage.sh status   # Check status
./manage.sh logs     # View logs
./manage.sh restart  # Restart services
./update.sh          # Deploy updates
```

### Monitoring
```bash
./manage.sh status   # Service status
./manage.sh logs     # Live logs
./manage.sh errors   # Recent errors
./manage.sh test     # Test endpoints
```

### Maintenance
```bash
./manage.sh backup   # Backup database
./update.sh          # Update application
```

## 🔍 Finding What You Need

| Need | File |
|------|------|
| How to deploy | `EC2_DEPLOYMENT.md` |
| Quick commands | `QUICKSTART_EC2.md` |
| What changed | `MIGRATION_GUIDE.md` |
| Environment vars | `backend/.env.example` |
| Nginx setup | `nginx.conf` |
| Service config | `sequoalpha.service` |
| First deploy | `deploy_ec2.sh` |
| Updates | `update.sh` |
| Daily tasks | `manage.sh` |
| S3 setup | `AWS_S3_SETUP.md` |

## 💡 Pro Tips

1. **Always check logs first**: `./manage.sh logs`
2. **Test after changes**: `./manage.sh test`
3. **Backup before updates**: `./manage.sh backup`
4. **Keep .env secure**: Never commit to git
5. **Use update.sh**: Don't manually restart services
6. **Monitor status**: Regular `./manage.sh status` checks

## 📞 Getting Help

1. Check logs: `./manage.sh logs`
2. Check status: `./manage.sh status`
3. Review `EC2_DEPLOYMENT.md` troubleshooting section
4. Check nginx logs: `sudo tail -f /var/log/nginx/error.log`
5. Check database: `sudo -u postgres psql sequoalpha`

---

**Remember**: Keep this file as your quick reference guide for EC2 deployment!

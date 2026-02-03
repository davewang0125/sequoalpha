# 🚀 SequoAlpha Management System

Sistema de gestión de documentos y usuarios para SequoAlpha Management LLC.

## 📋 Características

- ✅ **Autenticación segura** con JWT
- ✅ **Gestión de usuarios** (Admin puede crear usuarios)
- ✅ **Centro de documentos** con upload de PDFs y links externos
- ✅ **Base de datos persistente** (SQLite en desarrollo, PostgreSQL en producción)
- ✅ **Interfaz moderna** con React
- ✅ **Responsive design** para móviles y desktop

## 🏗️ Arquitectura

### Producción (EC2 - Recomendado)
```
Internet → EC2 Instance
          ├── Nginx (Port 80/443) → Frontend + Backend API
          ├── Gunicorn (Port 8000) → Flask Application
          ├── PostgreSQL (Local or RDS)
          └── AWS S3 (File Storage)
```

### Desarrollo Local
```
Frontend (localhost:8080) ←→ Backend (localhost:8000) ←→ SQLite
```

## 🚀 Deployment Options

### ⭐ Opción 1: AWS EC2 (Recomendado)

Despliegue completo en un servidor EC2 con control total.

**Quick Start:**
```bash
# En tu instancia EC2
git clone https://github.com/yourusername/sequoalpha.git
cd sequoalpha
sudo ./deploy_ec2.sh
```

📖 **Documentación completa**: [EC2_DEPLOYMENT.md](EC2_DEPLOYMENT.md)  
🚀 **Guía rápida**: [QUICKSTART_EC2.md](QUICKSTART_EC2.md)  
📋 **Referencia de archivos**: [FILE_REFERENCE.md](FILE_REFERENCE.md)

**Ventajas:**
- ✅ Control total del servidor
- ✅ Sin límites de tiempo de ejecución
- ✅ Mejor rendimiento
- ✅ Costos predecibles (~$20-50/mes)

### Opción 2: Render + Netlify (Legacy)

Despliegue en servicios managed (más limitado).

Ver [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) para instrucciones.

### Para desarrollo local:
```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Frontend (en otra terminal)
python3 -m http.server 8080
```

## 🔐 Credenciales por Defecto

- **Admin**: `admin` / `admin123`
- **Usuario**: `user` / `user123`

## 📁 Estructura del Proyecto

```
sequoalpha/
├── 📚 Documentation
│   ├── EC2_DEPLOYMENT.md          # Guía completa para EC2
│   ├── QUICKSTART_EC2.md          # Referencia rápida EC2
│   ├── MIGRATION_GUIDE.md         # Migración Render→EC2
│   ├── FILE_REFERENCE.md          # Guía de archivos
│   └── AWS_S3_SETUP.md            # Configuración S3
│
├── ⚙️ Configuration
│   ├── nginx.conf                 # Nginx para EC2
│   ├── sequoalpha.service         # Systemd service
│   ├── backend/.env.example       # Template variables
│   └── frontend/js/config.js      # Frontend config
│
├── 🔧 Scripts
│   ├── deploy_ec2.sh              # Despliegue EC2
│   ├── update.sh                  # Actualizar app
│   └── manage.sh                  # Gestión servicios
│
├── backend/                       # Backend Flask
│   ├── main.py                    # Aplicación principal
│   ├── models.py                  # Modelos de base de datos
│   ├── init_db.py                 # Inicialización de datos
│   ├── s3_config.py               # Configuración S3
│   ├── requirements.txt           # Dependencias Python
│   └── uploads/                   # Almacenamiento archivos
│
└── frontend/                      # Frontend
    ├── index.html                 # Página principal
    ├── js/                        # Componentes React
    │   ├── App.js
    │   ├── Login.js
    │   ├── Dashboard.js
    │   ├── UserDashboard.js
    │   └── DocumentCenter.js
    ├── css/                       # Estilos
    └── images/                    # Imágenes
```

## 🛠️ Tecnologías

- **Backend**: Flask, SQLAlchemy, JWT, bcrypt, Gunicorn
- **Frontend**: React, HTML5, CSS3
- **Base de datos**: PostgreSQL (producción), SQLite (desarrollo)
- **Storage**: AWS S3 (archivos)
- **Web Server**: Nginx (reverse proxy)
- **Despliegue**: AWS EC2, Systemd

## 🚀 Quick Start

### 🐳 Opción 1: Docker (Más Fácil - Recomendado para Testing)

Prueba la aplicación localmente con Docker antes de desplegar:

```bash
# Iniciar todo (PostgreSQL + Backend + Frontend)
docker-compose up --build -d

# Abrir en navegador
open http://localhost:8080

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

📖 **Guía completa**: [DOCKER_README.md](DOCKER_README.md)

### Desarrollo Local (Sin Docker)
```bash
# 1. Clone el repositorio
git clone https://github.com/yourusername/sequoalpha.git
cd sequoalpha

# 2. Setup Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tus configuraciones
python init_db.py
python main.py

# 3. Setup Frontend (en otra terminal)
cd ..
python3 -m http.server 8080

# 4. Abrir navegador
# http://localhost:8080
```

### Producción EC2
```bash
# 1. Conectar a EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Clonar y desplegar
git clone https://github.com/yourusername/sequoalpha.git
cd sequoalpha
sudo ./deploy_ec2.sh

# 3. Configurar
nano backend/.env
sudo nano /etc/nginx/sites-available/sequoalpha

# 4. Reiniciar servicios
sudo systemctl restart sequoalpha nginx

# Ver: EC2_DEPLOYMENT.md para detalles completos
```

## 📋 Gestión del Servidor (EC2)

```bash
# Estado de servicios
./manage.sh status

# Ver logs en tiempo real
./manage.sh logs

# Reiniciar servicios
./manage.sh restart

# Actualizar aplicación
./update.sh

# Crear backup
./manage.sh backup
```

## 📞 Contacto

- **Dirección**: 319 N Bernardo Ave, Mountainview, CA 94043
- **Teléfono**: 650-308-9049
- **Email**: info@sequoalpha.com

## 📄 Licencia

© 2025 SequoAlpha Management LP. All rights reserved.

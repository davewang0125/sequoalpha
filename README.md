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

```
Frontend (Netlify) ←→ Backend (Render) ←→ PostgreSQL (Render)
```

## 🚀 Despliegue Automático

### Para desarrollo local:
```bash
# Backend
cd backend
python main.py

# Frontend
python -m http.server 8080
```

### Para producción:
El sistema está configurado para despliegue automático en:
- **Frontend**: Netlify
- **Backend**: Render con PostgreSQL

Ver [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) para instrucciones detalladas.

## 🔐 Credenciales por Defecto

- **Admin**: `admin` / `admin123`
- **Usuario**: `user` / `user123`

## 📁 Estructura del Proyecto

```
sequoalpha/
├── backend/                 # Backend Flask
│   ├── main.py             # Aplicación principal
│   ├── models.py           # Modelos de base de datos
│   ├── init_db.py          # Inicialización de datos
│   ├── start.sh            # Script de inicio para Render
│   ├── requirements.txt    # Dependencias de desarrollo
│   ├── requirements-prod.txt # Dependencias de producción
│   └── render.yaml         # Configuración de Render
├── frontend/               # Frontend React
│   └── js/
│       ├── App.js          # Componente principal
│       ├── Login.js        # Componente de login
│       ├── Dashboard.js    # Dashboard principal
│       ├── DocumentCenter.js # Centro de documentos
│       └── config.js       # Configuración de URLs
├── index.html              # Página principal
└── README.md               # Este archivo
```

## 🛠️ Tecnologías

- **Backend**: Flask, SQLAlchemy, JWT, bcrypt
- **Frontend**: React, HTML5, CSS3
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Despliegue**: Render, Netlify

## 📞 Contacto

- **Dirección**: 319 N Bernardo Ave, Mountainview, CA 94043
- **Teléfono**: 650-308-9049
- **Email**: info@sequoalpha.com

## 📄 Licencia

© 2025 SequoAlpha Management LP. All rights reserved.

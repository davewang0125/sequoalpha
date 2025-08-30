# 🚀 SequoAlpha - Render Deployment Guide

## Despliegue Automático en Render

### 📋 Requisitos Previos
- Cuenta en [Render.com](https://render.com)
- Repositorio conectado a GitHub

### 🔧 Configuración Automática

#### 1. Crear Web Service en Render
1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Haz clic en "New +" → "Web Service"
3. Conecta tu repositorio: `https://github.com/kritux/sequoalpha.git`
4. Selecciona la rama: `Cristian`

#### 2. Configuración del Servicio
- **Name**: `sequoalpha-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r backend/requirements-prod.txt`
- **Start Command**: `cd backend && chmod +x start.sh && ./start.sh`
- **Root Directory**: `backend`

#### 3. Variables de Entorno
Render configurará automáticamente:
- `SECRET_KEY` - Generado automáticamente
- `PYTHON_VERSION` - 3.11.0
- `DATABASE_URL` - Conectado a PostgreSQL

#### 4. Base de Datos PostgreSQL
- Se creará automáticamente
- Se conectará al servicio web
- Los datos se inicializarán automáticamente

### 🎯 Configuración del Frontend

#### 1. Netlify (Ya configurado)
- El frontend se actualizará automáticamente
- Usará la URL de Render para el backend
- Configuración automática en `frontend/js/config.js`

#### 2. URLs de Producción
- **Frontend**: Tu sitio en Netlify
- **Backend**: `https://sequoalpha-backend.onrender.com`
- **Base de datos**: PostgreSQL en Render

### ✅ Verificación del Despliegue

#### 1. Probar la API
```bash
curl https://sequoalpha-backend.onrender.com/
```
Debería devolver: `{"message":"SequoAlpha Management API - Secure Access Only"}`

#### 2. Probar el Login
- Ve a tu sitio en Netlify
- Login con: `admin` / `admin123`
- Deberías acceder al dashboard

#### 3. Probar Document Center
- Solo para usuarios admin
- Deberías ver documentos de ejemplo
- Funcionalidad de upload y links

### 🔧 Estructura de Archivos

```
sequoalpha/
├── backend/
│   ├── main.py              # Aplicación Flask
│   ├── models.py            # Modelos de base de datos
│   ├── init_db.py           # Inicialización de datos
│   ├── start.sh             # Script de inicio
│   ├── requirements-prod.txt # Dependencias de producción
│   └── render.yaml          # Configuración de Render
├── frontend/
│   └── js/
│       └── config.js        # Configuración de URLs
└── index.html               # Página principal
```

### 🚨 Solución de Problemas

#### Si el backend no responde:
1. Verifica los logs en Render Dashboard
2. Asegúrate de que la base de datos esté conectada
3. Verifica que las variables de entorno estén configuradas

#### Si el frontend no puede conectar:
1. Verifica que la URL del backend sea correcta
2. Asegúrate de que CORS esté configurado
3. Verifica que el token se esté enviando correctamente

### 📞 Credenciales por Defecto
- **Admin**: `admin` / `admin123`
- **Usuario**: `user` / `user123`

### 🎉 ¡Listo!
Una vez desplegado, tu sistema estará completamente funcional en la nube con:
- ✅ Backend en Render con PostgreSQL
- ✅ Frontend en Netlify
- ✅ Base de datos persistente
- ✅ Autenticación segura
- ✅ Gestión de documentos

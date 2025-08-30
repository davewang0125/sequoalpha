# 🚀 SequoAlpha Backend Deployment Guide

## Despliegue en Render (Recomendado)

### 1. Crear cuenta en Render
- Ve a [render.com](https://render.com)
- Crea una cuenta gratuita

### 2. Conectar tu repositorio
- Haz clic en "New +" → "Web Service"
- Conecta tu repositorio de GitHub: `https://github.com/kritux/sequoalpha.git`
- Selecciona la rama `Cristian`

### 3. Configurar el servicio
- **Name**: `sequoalpha-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && gunicorn main:app`
- **Root Directory**: `backend`

### 4. Variables de entorno
- **SECRET_KEY**: (se genera automáticamente)
- **PYTHON_VERSION**: `3.11.0`

### 5. Desplegar
- Haz clic en "Create Web Service"
- Espera a que se complete el despliegue (5-10 minutos)

### 6. Obtener la URL
- Una vez desplegado, obtendrás una URL como: `https://sequoalpha-backend.onrender.com`
- Esta URL se usará automáticamente en el frontend

## Actualizar el Frontend

### 1. Subir cambios al repositorio
```bash
git add .
git commit -m "Add backend deployment configuration"
git push origin Cristian
```

### 2. El frontend en Netlify se actualizará automáticamente

## Verificar el despliegue

### 1. Probar la API
- Ve a: `https://sequoalpha-backend.onrender.com/`
- Deberías ver: `{"message": "SequoAlpha Management API - Secure Access Only"}`

### 2. Probar el login
- Ve a tu sitio en Netlify
- Intenta hacer login con:
  - Usuario: `admin`
  - Contraseña: `admin123`

## Credenciales por defecto
- **Admin**: `admin` / `admin123`
- **Usuario**: `user` / `user123`

## Solución de problemas

### Si el backend no responde:
1. Verifica los logs en Render
2. Asegúrate de que el puerto esté configurado correctamente
3. Verifica que las variables de entorno estén configuradas

### Si el frontend no puede conectar:
1. Verifica que la URL del backend sea correcta
2. Asegúrate de que CORS esté configurado
3. Verifica que el token se esté enviando correctamente

#!/usr/bin/env python3
"""
Script de prueba detallado para identificar problemas en el registro
"""

import requests
import json
import traceback

# Configuración
BASE_URL = "http://127.0.0.1:8000"
REGISTER_URL = f"{BASE_URL}/auth/register"

def test_register_detailed():
    """Prueba el registro con más detalles"""
    print("🔐 Probando registro de usuario con detalles...")
    
    user_data = {
        "name": "Usuario Test",
        "email": "test@example.com",
        "password": "password123"
    }
    
    print(f"📤 Datos a enviar: {json.dumps(user_data, indent=2)}")
    print(f"📤 URL: {REGISTER_URL}")
    
    try:
        response = requests.post(REGISTER_URL, json=user_data)
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response headers: {dict(response.headers)}")
        print(f"📥 Response body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registro exitoso!")
            user_data = response.json()
            print(f"👤 Usuario creado: {json.dumps(user_data, indent=2)}")
            return user_data
        elif response.status_code == 500:
            print("❌ Error interno del servidor (500)")
            print("💡 Esto indica un problema en el código del backend")
            return None
        else:
            print(f"❌ Error en el registro: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print(f"📋 Traceback completo:")
        traceback.print_exc()
        return None

def test_backend_health():
    """Prueba la salud del backend"""
    print("\n🏥 Probando salud del backend...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"📥 Root endpoint status: {response.status_code}")
        print(f"📥 Root endpoint body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Backend está saludable")
            return True
        else:
            print("❌ Backend no está saludable")
            return False
            
    except Exception as e:
        print(f"❌ Error accediendo al backend: {e}")
        return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("\n🗄️ Probando conexión a la base de datos...")
    
    try:
        from app.database import SessionLocal
        from app.models.user import User
        
        db = SessionLocal()
        try:
            # Intentar hacer una consulta simple
            users = db.query(User).limit(1).all()
            print(f"✅ Conexión a la base de datos exitosa")
            print(f"📊 Usuarios en la base de datos: {len(users)}")
            return True
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error en la base de datos: {e}")
        print(f"📋 Traceback completo:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas detalladas del registro...")
    print(f"🌐 URL base: {BASE_URL}")
    
    # Probar salud del backend
    backend_ok = test_backend_health()
    
    if backend_ok:
        # Probar conexión a la base de datos
        db_ok = test_database_connection()
        
        if db_ok:
            # Probar registro
            test_register_detailed()
        else:
            print("❌ No se puede continuar debido a problemas en la base de datos")
    else:
        print("❌ No se puede continuar debido a problemas en el backend")
    
    print("\n🏁 Pruebas detalladas completadas!")

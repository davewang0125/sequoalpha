#!/usr/bin/env python3
"""
Script de prueba para registrar un nuevo usuario con email diferente
"""

import requests
import json

# Configuración
BASE_URL = "http://127.0.0.1:8000"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"

def test_register_new_user():
    """Prueba el registro de un nuevo usuario con email diferente"""
    print("🔐 Probando registro de nuevo usuario...")
    
    user_data = {
        "name": "Usuario Nuevo",
        "email": "nuevo@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(REGISTER_URL, json=user_data)
        print(f"📤 Request enviado a: {REGISTER_URL}")
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registro exitoso!")
            user_data = response.json()
            print(f"👤 Usuario creado: {json.dumps(user_data, indent=2)}")
            return user_data
        else:
            print(f"❌ Error en el registro: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_login_new_user():
    """Prueba el login del nuevo usuario"""
    print("\n🔑 Probando login del nuevo usuario...")
    
    login_data = {
        "email": "nuevo@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"📤 Request enviado a: {LOGIN_URL}")
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login exitoso!")
            token_data = response.json()
            print(f"🎫 Token: {json.dumps(token_data, indent=2)}")
            return token_data
        else:
            print("❌ Error en el login")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de registro de nuevo usuario...")
    print(f"🌐 URL base: {BASE_URL}")
    
    # Probar registro
    user = test_register_new_user()
    
    if user:
        # Probar login
        test_login_new_user()
    else:
        print("❌ No se pudo crear el usuario para continuar con las pruebas")
    
    print("\n🏁 Pruebas completadas!")

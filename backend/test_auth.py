#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de autenticación
"""

import requests
import json

# Configuración
BASE_URL = "http://127.0.0.1:8000"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"

def test_register():
    """Prueba el registro de un nuevo usuario"""
    print("🔐 Probando registro de usuario...")
    
    user_data = {
        "name": "Usuario Test",
        "email": "test@example.com",
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
            print(f"👤 Usuario creado: {user_data}")
            return user_data
        else:
            print("❌ Error en el registro")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_login():
    """Prueba el login del usuario"""
    print("\n🔑 Probando login de usuario...")
    
    login_data = {
        "email": "test@example.com",
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
            print(f"🎫 Token: {token_data}")
            return token_data
        else:
            print("❌ Error en el login")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_protected_endpoint(token):
    """Prueba un endpoint protegido"""
    print("\n🛡️ Probando endpoint protegido...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"📤 Request enviado a: {BASE_URL}/users/me")
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Endpoint protegido accesible!")
            return True
        else:
            print("❌ Error accediendo al endpoint protegido")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de autenticación...")
    print(f"🌐 URL base: {BASE_URL}")
    
    # Probar registro
    user = test_register()
    
    if user:
        # Probar login
        token_data = test_login()
        
        if token_data and "access_token" in token_data:
            # Probar endpoint protegido
            test_protected_endpoint(token_data["access_token"])
        else:
            print("❌ No se pudo obtener el token para probar endpoints protegidos")
    else:
        print("❌ No se pudo crear el usuario para continuar con las pruebas")
    
    print("\n🏁 Pruebas completadas!")

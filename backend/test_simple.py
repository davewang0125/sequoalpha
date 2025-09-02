#!/usr/bin/env python3
"""
Script de prueba simple para verificar si el backend responde
"""

import requests
import time

def test_backend():
    """Prueba si el backend responde"""
    print("🔍 Probando si el backend responde...")
    
    try:
        # Probar el endpoint raíz
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Backend responde correctamente!")
            return True
        else:
            print("❌ Backend responde pero con error")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_docs():
    """Prueba si la documentación está disponible"""
    print("\n📚 Probando documentación...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/docs", timeout=5)
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Documentación disponible!")
            return True
        else:
            print("❌ Documentación no disponible")
            return False
            
    except Exception as e:
        print(f"❌ Error accediendo a la documentación: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas simples del backend...")
    
    # Esperar un momento para que el backend se inicie
    print("⏳ Esperando 3 segundos para que el backend se inicie...")
    time.sleep(3)
    
    # Probar si el backend responde
    backend_ok = test_backend()
    
    if backend_ok:
        # Probar documentación
        test_docs()
    else:
        print("\n💡 Sugerencias:")
        print("1. Verifica que el backend esté ejecutándose")
        print("2. Verifica que no haya errores en la consola del backend")
        print("3. Verifica que el puerto 8000 esté disponible")
    
    print("\n🏁 Pruebas completadas!")

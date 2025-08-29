#!/usr/bin/env python3
"""
Script para probar directamente la creación de usuarios en la base de datos
"""

import sys
import traceback

def test_user_creation():
    """Prueba la creación de usuarios directamente en la base de datos"""
    print("🔐 Probando creación de usuario directamente en la base de datos...")
    
    try:
        from app.database import SessionLocal
        from app.models.user import User
        from app.crud.user import create_user
        from app.schemas.user import UserCreate
        
        print("✅ Imports exitosos")
        
        # Crear sesión de base de datos
        db = SessionLocal()
        print("✅ Sesión de base de datos creada")
        
        try:
            # Crear datos de usuario
            user_data = UserCreate(
                name="Usuario Test",
                email="test@example.com",
                password="password123"
            )
            print(f"✅ Datos de usuario creados: {user_data}")
            
            # Crear usuario usando CRUD
            user = create_user(db, user_data)
            print(f"✅ Usuario creado exitosamente: {user}")
            
            # Verificar que se puede convertir a UserOut
            from app.schemas.user import UserOut
            user_out = UserOut.model_validate(user)
            print(f"✅ Usuario convertido a UserOut: {user_out}")
            
            return True
            
        finally:
            db.close()
            print("✅ Sesión de base de datos cerrada")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"📋 Traceback completo:")
        traceback.print_exc()
        return False

def test_database_models():
    """Prueba que todos los modelos se puedan importar y usar"""
    print("\n🗄️ Probando modelos de base de datos...")
    
    try:
        from app.models import User, Service, ClientService, PrintOrder
        print("✅ Todos los modelos importados correctamente")
        
        # Verificar que se pueden crear instancias
        user = User(name="Test", email="test@test.com", hashed_password="hash")
        print("✅ Instancia de User creada correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con modelos: {e}")
        print(f"📋 Traceback completo:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas directas de creación de usuarios...")
    
    # Probar modelos
    models_ok = test_database_models()
    
    if models_ok:
        # Probar creación de usuario
        test_user_creation()
    else:
        print("❌ No se puede continuar debido a problemas con los modelos")
    
    print("\n🏁 Pruebas directas completadas!")

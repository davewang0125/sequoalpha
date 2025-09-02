#!/usr/bin/env python3
"""
Script para inicializar la base de datos SQLite para Growth Bizon Print
Este script crea todas las tablas necesarias para el proyecto de impresión láser
"""

import os
import sys

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.models import *  # Importar todos los modelos

def initialize_db():
    """Inicializar la base de datos SQLite y crear tablas"""
    print("🚀 Iniciando la inicialización de la base de datos SQLite...")
    
    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente en la base de datos SQLite.")
        print("📁 Base de datos: growth_bizon_print.db")
        
        # Crear directorio de uploads si no existe
        uploads_dir = "uploads"
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
            print("✅ Directorio de uploads creado.")
        
    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
        sys.exit(1)

if __name__ == "__main__":
    initialize_db()

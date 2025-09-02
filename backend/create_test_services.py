#!/usr/bin/env python3
"""
Script para crear servicios de prueba en la base de datos
"""

from app.database import SessionLocal
from app.models.service import Service
from app.schemas.service import ServiceCreate

def create_test_services():
    """Crea servicios de prueba"""
    print("🚀 Creando servicios de prueba...")
    
    # Datos de servicios de prueba
    test_services = [
        {
            "name": "Grabado Láser en Madera",
            "description": "Servicio de grabado láser profesional en superficies de madera",
            "base_price": 2.50,  # precio por cm²
            "pasos_flujo": [
                {"nombre": "Recepción de archivo", "descripcion": "Recibir y validar archivo del cliente", "estado": "pendiente"},
                {"nombre": "Preparación de material", "descripcion": "Seleccionar y preparar la madera", "estado": "pendiente"},
                {"nombre": "Configuración láser", "descripcion": "Ajustar parámetros del láser", "estado": "pendiente"},
                {"nombre": "Grabado", "descripcion": "Ejecutar el grabado láser", "estado": "pendiente"},
                {"nombre": "Acabado", "descripcion": "Aplicar acabados finales", "estado": "pendiente"},
                {"nombre": "Control de calidad", "descripcion": "Verificar resultado final", "estado": "pendiente"},
                {"nombre": "Empaque", "descripcion": "Empacar para envío", "estado": "pendiente"}
            ],
            "is_active": True
        },
        {
            "name": "Corte Láser en Madera",
            "description": "Servicio de corte láser preciso en madera",
            "base_price": 3.00,  # precio por cm²
            "pasos_flujo": [
                {"nombre": "Recepción de archivo", "descripcion": "Recibir archivo vectorial", "estado": "pendiente"},
                {"nombre": "Optimización de rutas", "descripcion": "Optimizar rutas de corte", "estado": "pendiente"},
                {"nombre": "Configuración láser", "descripcion": "Ajustar potencia y velocidad", "estado": "pendiente"},
                {"nombre": "Corte", "descripcion": "Ejecutar corte láser", "estado": "pendiente"},
                {"nombre": "Limpieza", "descripcion": "Limpiar residuos", "estado": "pendiente"},
                {"nombre": "Control de calidad", "descripcion": "Verificar precisión del corte", "estado": "pendiente"},
                {"nombre": "Empaque", "descripcion": "Empacar piezas cortadas", "estado": "pendiente"}
            ],
            "is_active": True
        },
        {
            "name": "Marcado Láser en Madera",
            "description": "Servicio de marcado láser para identificación",
            "base_price": 1.50,  # precio por cm²
            "pasos_flujo": [
                {"nombre": "Recepción de archivo", "descripcion": "Recibir archivo de marcado", "estado": "pendiente"},
                {"nombre": "Preparación de superficie", "descripcion": "Limpiar y preparar madera", "estado": "pendiente"},
                {"nombre": "Configuración láser", "descripcion": "Ajustar parámetros de marcado", "estado": "pendiente"},
                {"nombre": "Marcado", "descripcion": "Ejecutar marcado láser", "estado": "pendiente"},
                {"nombre": "Acabado", "descripcion": "Aplicar sellador si es necesario", "estado": "pendiente"},
                {"nombre": "Control de calidad", "descripcion": "Verificar legibilidad", "estado": "pendiente"},
                {"nombre": "Empaque", "descripcion": "Empacar producto final", "estado": "pendiente"}
            ],
            "is_active": True
        }
    ]
    
    db = SessionLocal()
    try:
        for service_data in test_services:
            # Verificar si el servicio ya existe
            existing_service = db.query(Service).filter(Service.name == service_data["name"]).first()
            
            if existing_service:
                print(f"⚠️ Servicio '{service_data['name']}' ya existe, saltando...")
                continue
            
            # Crear servicio
            service = Service(**service_data)
            db.add(service)
            print(f"✅ Servicio '{service_data['name']}' creado exitosamente")
        
        db.commit()
        print("🎉 Todos los servicios de prueba creados exitosamente")
        
        # Mostrar servicios creados
        services = db.query(Service).all()
        print(f"\n📊 Total de servicios en la base de datos: {len(services)}")
        for service in services:
            print(f"   • {service.name} - ${service.base_price}/cm² - Activo: {service.is_active}")
            
    except Exception as e:
        print(f"❌ Error creando servicios: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_services()

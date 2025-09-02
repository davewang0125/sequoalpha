#!/usr/bin/env python3
"""
Script de depuración completa del backend
Prueba todos los endpoints y funcionalidades
"""

import requests
import json
import time
from typing import Dict, List, Any

# Configuración
BASE_URL = "http://127.0.0.1:8000"

class BackendDebugger:
    def __init__(self):
        self.results = {}
        self.auth_token = None
        self.test_user = None
        
    def log(self, message: str, level: str = "INFO"):
        """Log con timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, 
                     headers: Dict = None, expected_status: int = 200) -> Dict:
        """Prueba un endpoint específico"""
        url = f"{BASE_URL}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return {"success": False, "error": f"Método {method} no soportado"}
            
            success = response.status_code == expected_status
            result = {
                "success": success,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response": response.text[:500] if response.text else "",
                "headers": dict(response.headers)
            }
            
            if success:
                self.log(f"✅ {method} {endpoint} - Status: {response.status_code}")
            else:
                self.log(f"❌ {method} {endpoint} - Status: {response.status_code} (esperado: {expected_status})")
                if response.text:
                    self.log(f"   Response: {response.text[:200]}...", "ERROR")
            
            return result
            
        except Exception as e:
            self.log(f"❌ {method} {endpoint} - Error: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    def test_public_endpoints(self):
        """Prueba endpoints públicos"""
        self.log("🔍 Probando endpoints públicos...")
        
        endpoints = [
            ("GET", "/", {}, 200),
            ("GET", "/docs", {}, 200),
            ("GET", "/openapi.json", {}, 200),
        ]
        
        for method, endpoint, data, expected_status in endpoints:
            result = self.test_endpoint(method, endpoint, data, expected_status=expected_status)
            self.results[f"{method}_{endpoint}"] = result
    
    def test_auth_endpoints(self):
        """Prueba endpoints de autenticación"""
        self.log("🔐 Probando endpoints de autenticación...")
        
        # Crear usuario de prueba con email único
        import time
        timestamp = int(time.time())
        test_user_data = {
            "name": "Usuario Debug",
            "email": f"debug{timestamp}@test.com",
            "password": "debug123"
        }
        
        # Probar registro
        register_result = self.test_endpoint("POST", "/auth/register", test_user_data, expected_status=200)
        self.results["auth_register"] = register_result
        
        if register_result["success"]:
            self.test_user = test_user_data
            self.log("✅ Usuario de prueba creado exitosamente")
            
            # Probar login
            login_data = {
                "email": test_user_data["email"],
                "password": test_user_data["password"]
            }
            
            login_result = self.test_endpoint("POST", "/auth/login", login_data, expected_status=200)
            self.results["auth_login"] = login_result
            
            if login_result["success"]:
                try:
                    token_data = json.loads(login_result["response"])
                    self.auth_token = token_data.get("access_token")
                    self.log("✅ Token de autenticación obtenido")
                except:
                    self.log("❌ No se pudo obtener el token del login", "ERROR")
        else:
            self.log("❌ No se pudo crear usuario de prueba", "ERROR")
    
    def test_protected_endpoints(self):
        """Prueba endpoints protegidos"""
        if not self.auth_token:
            self.log("❌ No hay token de autenticación para probar endpoints protegidos", "ERROR")
            return
        
        self.log("🛡️ Probando endpoints protegidos...")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        protected_endpoints = [
            ("GET", "/users/me", {}, headers, 200),
            ("GET", "/users/admin-only", {}, headers, 403),  # Usuario cliente no debería tener acceso
        ]
        
        for method, endpoint, data, headers, expected_status in protected_endpoints:
            result = self.test_endpoint(method, endpoint, data, headers, expected_status)
            self.results[f"protected_{method}_{endpoint}"] = result
    
    def test_service_endpoints(self):
        """Prueba endpoints de servicios"""
        self.log("🛠️ Probando endpoints de servicios...")
        
        endpoints = [
            ("GET", "/services/", {}, 200),
        ]
        
        for method, endpoint, data, expected_status in endpoints:
            result = self.test_endpoint(method, endpoint, data, expected_status=expected_status)
            self.results[f"services_{method}_{endpoint}"] = result
    
    def test_print_order_endpoints(self):
        """Prueba endpoints de órdenes de impresión"""
        self.log("🖨️ Probando endpoints de órdenes de impresión...")
        
        if not self.auth_token:
            self.log("❌ No hay token para probar endpoints de órdenes", "ERROR")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Probar obtener órdenes del usuario (endpoint correcto)
        result = self.test_endpoint("GET", "/print-orders/", {}, headers, 200)
        self.results["print_orders_user_orders"] = result
    
    def test_admin_endpoints(self):
        """Prueba endpoints de administración"""
        self.log("👑 Probando endpoints de administración...")
        
        if not self.auth_token:
            self.log("❌ No hay token para probar endpoints de admin", "ERROR")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Usuario cliente no debería tener acceso a endpoints de admin
        admin_endpoints = [
            ("GET", "/admin/orders", {}, headers, 403),
            ("GET", "/admin/users", {}, headers, 403),
        ]
        
        for method, endpoint, data, headers, expected_status in admin_endpoints:
            result = self.test_endpoint(method, endpoint, data, headers, expected_status)
            self.results[f"admin_{method}_{endpoint}"] = result
    
    def generate_report(self):
        """Genera un reporte de la depuración"""
        self.log("📊 Generando reporte de depuración...")
        
        total_tests = len(self.results)
        successful_tests = sum(1 for result in self.results.values() if result.get("success", False))
        failed_tests = total_tests - successful_tests
        
        print("\n" + "="*60)
        print("📋 REPORTE DE DEPURACIÓN DEL BACKEND")
        print("="*60)
        print(f"📊 Total de pruebas: {total_tests}")
        print(f"✅ Exitosas: {successful_tests}")
        print(f"❌ Fallidas: {failed_tests}")
        print(f"📈 Tasa de éxito: {(successful_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ PRUEBAS FALLIDAS:")
            for test_name, result in self.results.items():
                if not result.get("success", False):
                    print(f"   • {test_name}: {result.get('error', 'Status code incorrecto')}")
        
        print("\n✅ PRUEBAS EXITOSAS:")
        for test_name, result in self.results.items():
            if result.get("success", False):
                print(f"   • {test_name}")
        
        print("\n" + "="*60)
        
        return {
            "total": total_tests,
            "successful": successful_tests,
            "failed": failed_tests,
            "success_rate": successful_tests/total_tests*100
        }
    
    def run_full_debug(self):
        """Ejecuta la depuración completa"""
        self.log("🚀 Iniciando depuración completa del backend...")
        
        try:
            # Probar endpoints públicos
            self.test_public_endpoints()
            
            # Probar autenticación
            self.test_auth_endpoints()
            
            # Probar endpoints protegidos
            self.test_protected_endpoints()
            
            # Probar endpoints de servicios
            self.test_service_endpoints()
            
            # Probar endpoints de órdenes
            self.test_print_order_endpoints()
            
            # Probar endpoints de admin
            self.test_admin_endpoints()
            
            # Generar reporte
            report = self.generate_report()
            
            self.log("🏁 Depuración completa finalizada")
            return report
            
        except Exception as e:
            self.log(f"❌ Error durante la depuración: {str(e)}", "ERROR")
            return None

if __name__ == "__main__":
    debugger = BackendDebugger()
    debugger.run_full_debug()

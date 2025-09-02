from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth
from .api import users
from .api import client_services
from .api import services
from .api import admin
from .api import print_orders
# Importar todos los modelos para asegurar que estén registrados
from . import models

app = FastAPI(
    title="Growth Bizon Print API",
    description="API para servicios de impresión láser en madera",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(client_services.router)
app.include_router(services.router)
app.include_router(admin.router)
app.include_router(print_orders.router)

@app.get("/")
def read_root():
    return {
        "message": "Growth Bizon Print API",
        "version": "1.0.0",
        "docs": "/docs"
    } 
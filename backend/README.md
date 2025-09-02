# Growth Bizon Backend

## Requisitos
- Python 3.9+
- PostgreSQL

## Instalación

```bash
pip install -r requirements.txt
```

## Variables de entorno
Crea un archivo `.env` en `backend/app/` con:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=growthbizon
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
SECRET_KEY=alguna_clave_secreta
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

## Migraciones

```bash
alembic upgrade head
``` 

## Seguridad en el registro de usuarios
- El campo "rol" NO está disponible para los usuarios al registrarse.
- Todos los registros públicos serán asignados automáticamente como "cliente".
- Solo un admin, desde un endpoint protegido, puede crear usuarios con rol "admin". 
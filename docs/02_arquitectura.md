# Arquitectura del Sistema

## Backend
- Framework: Flask
- Lenguaje: Python
- ORM: SQLAlchemy
- Migraciones: Alembic

## Frontend
- HTML + Jinja2
- CSS personalizado
- JavaScript básico

## Base de datos
- PostgreSQL

## Estructura del proyecto

app/
├── middleware/
├── models/
├── routes/
├── services/
├── templates/
├── static/
├── utils/

## Capas

1. Presentación (templates)
2. Lógica (routes + services)
3. Datos (models)

## Seguridad
- Middleware de autenticación
- Middleware de superusuario
- Control de acceso por permisos
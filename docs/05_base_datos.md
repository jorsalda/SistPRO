# Base de Datos

## Motor
PostgreSQL

## Tablas principales

### usuario
- id
- email
- password
- rol

### docente
- id
- nombre
- especialidad

### colegio
- id
- nombre

### permiso
- id
- nombre
- descripcion

## Relaciones
- Usuario ↔ Permisos
- Docente ↔ Colegio

## Migraciones
Manejadas con Alembic
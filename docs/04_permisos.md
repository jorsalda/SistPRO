# Sistema de Permisos

## Descripción
El sistema controla el acceso a funcionalidades según el rol del usuario.

## Tipos de usuario
- Administrador
- Docente
- Usuario básico

## Implementación
- Middleware de autenticación
- Middleware de superusuario

## Ejemplo de permisos
- Ver docentes
- Crear docentes
- Editar permisos
- Acceso a dashboard

## Flujo
1. Usuario inicia sesión
2. Middleware valida autenticación
3. Se verifican permisos
4. Se permite o bloquea acceso
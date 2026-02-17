from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from app.models.usuario import Usuario
from app.models.colegio import Colegio
from app.extensions import db
from app.utils.password_validator import validar_contrasena
from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def login_usuario(email, password):
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return False, "Usuario no encontrado"

    if not check_password_hash(usuario.password_hash, password):
        return False, "Contraseña incorrecta"

    # ✅ CORREGIDO: Usar is_active en lugar de estatus
    if not usuario.is_active:
        return False, "Usuario no activo"

    return True, usuario


def registrar_usuario(email, password, colegio_nombre):
    # ✅ VALIDAR CONTRASEÑA ANTES DE REGISTRAR
    es_valida, errores = validar_contrasena(password)

    if not es_valida:
        mensaje_error = "❌ Contraseña no válida:\n" + "\n".join([f"• {error}" for error in errores])
        return False, mensaje_error

    # Verificar si el email ya está registrado
    if Usuario.query.filter_by(email=email).first():
        return False, "El email ya está registrado"

    # Crear o obtener el colegio
    colegio = Colegio.query.filter_by(nombre=colegio_nombre).first()
    if not colegio:
        colegio = Colegio(nombre=colegio_nombre)
        db.session.add(colegio)
        db.session.commit()

    # ⭐⭐ DETERMINAR ROL: Primer usuario = admin, demás = colegio ⭐⭐
    total_usuarios = Usuario.query.count()
    es_admin = total_usuarios == 0

    # Crear el usuario
    usuario = Usuario(
        email=email,
        password_hash=generate_password_hash(password),
        colegio_id=colegio.id,
        fecha_registro=datetime.utcnow(),
        is_superadmin=es_admin,  # ⭐ Primer usuario = superadmin
        is_active=True,  # ⭐ Activo al registrarse
        is_approved=False,  # ⭐ No aprobado todavía
        dias_prueba=15,  # ⭐ 15 días de prueba
        fecha_expiracion=datetime.utcnow() + timedelta(days=15)  # ⭐ Fecha de expiración
    )

    db.session.add(usuario)
    db.session.commit()

    return True, "OK"


# ⭐⭐⭐ FUNCIONES PARA RESET DE CONTRASEÑA ⭐⭐⭐

def generar_token_reset(email):
    """Genera un token firmado y temporal para resetear contraseña"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')


def verificar_token_reset(token, expiration=3600):
    """Verifica y decodifica el token (expira en 1 hora por defecto)"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=expiration
        )
        return email
    except:
        return None


def resetear_contrasena_por_email(email, nueva_contrasena):
    """Resetea la contraseña de un usuario por email"""
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return False, "Usuario no encontrado"

    # Validar nueva contraseña
    es_valida, errores = validar_contrasena(nueva_contrasena)
    if not es_valida:
        mensaje_error = "❌ Contraseña no válida:\n" + "\n".join([f"• {error}" for error in errores])
        return False, mensaje_error

    # Actualizar contraseña
    usuario.password_hash = generate_password_hash(nueva_contrasena)
    db.session.commit()

    return True, "Contraseña actualizada exitosamente"



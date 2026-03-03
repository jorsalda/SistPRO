from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from app.models.usuario import Usuario
from app.extensions import db

MAX_INTENTOS = 5
TIEMPO_BLOQUEO_MIN = 2

def login_usuario(email, password):
    print("🔥 ENTRÓ A login_usuario 🔥", email)

def login_usuario(email, password):
    ahora = datetime.now()

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return False, "Credenciales inválidas"

    # 🔒 Ya está bloqueado
    if usuario.locked_until and usuario.locked_until > ahora:
        segundos = int((usuario.locked_until - ahora).total_seconds())
        return False, f"Usuario bloqueado. Intenta en {segundos} segundos"

    # 🔐 Contraseña incorrecta
    if not check_password_hash(usuario.password_hash, password):
        usuario.failed_attempts = (usuario.failed_attempts or 0) + 1

        # 🚨 LLEGÓ AL LÍMITE
        if usuario.failed_attempts >= MAX_INTENTOS:
            usuario.locked_until = ahora + timedelta(minutes=TIEMPO_BLOQUEO_MIN)
            db.session.commit()
            return False, (
                f"Usuario bloqueado temporalmente por exceder {MAX_INTENTOS} intentos. "
                f"Inténtalo nuevamente dentro de {TIEMPO_BLOQUEO_MIN} minutos."
            )

        db.session.commit()
        return False, "Credenciales inválidas"

    # 🚫 Usuario inactivo
    if not usuario.is_active:
        return False, "Usuario no activo"

    # ⏳ Cuenta expirada
    if usuario.fecha_expiracion and usuario.fecha_expiracion < ahora:
        return False, "Cuenta expirada. Contacte al administrador"

    # ✅ LOGIN EXITOSO → limpiar seguridad
    usuario.failed_attempts = 0
    usuario.locked_until = None
    db.session.commit()

    return True, usuario
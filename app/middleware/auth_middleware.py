from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from datetime import datetime


def acceso_permitido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        # Verificar si el usuario tiene el método puede_acceder
        if hasattr(current_user, 'puede_acceder'):
            puede_acceder, razon = current_user.puede_acceder()

            if not puede_acceder:
                flash(f'Acceso restringido: {razon}. Contacta al administrador.', 'danger')
                return redirect(url_for('auth.estado_cuenta'))

        # Si está en prueba, mostrar advertencia
        if not getattr(current_user, 'is_approved', False) and not getattr(current_user, 'is_superadmin', False):
            fecha_registro = getattr(current_user, 'fecha_registro', datetime.utcnow())
            dias_transcurridos = (datetime.utcnow() - fecha_registro).days
            dias_prueba = getattr(current_user, 'dias_prueba', 15)
            dias_restantes = dias_prueba - dias_transcurridos

            if dias_restantes <= 3 and dias_restantes > 0:
                flash(f'⚠️ Tu período de prueba termina en {dias_restantes} día(s). '
                      f'Solicita aprobación al administrador.', 'warning')

        return f(*args, **kwargs)

    return decorated_function
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.services.auth_service import login_usuario, registrar_usuario
from app.extensions import db
from datetime import datetime
from app.middleware.auth_middleware import acceso_permitido  # NUEVO IMPORT

auth_bp = Blueprint('auth', __name__)


# ⭐⭐ RUTA RAÍZ ⭐⭐
@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('docente.listar'))  # ✅ CORREGIDO: "listado"
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ok, resultado = login_usuario(
            request.form['email'],
            request.form['password']
        )

        if ok:
            login_user(resultado)
            return redirect(url_for('docente.listar'))  # ✅ CORREGIDO: ir a LISTA, no formulario

        flash(resultado, 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
@acceso_permitido  # ← NUEVA LÍNEA
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ok, mensaje = registrar_usuario(
            request.form['email'],
            request.form['password'],
            request.form['colegio']
        )

        if ok:
            flash("✅ Registro exitoso. Tienes 15 días de prueba gratuita. "
                  "Un administrador revisará tu cuenta pronto.", "success")  # ← MENSAJE MODIFICADO
            return redirect(url_for('auth.login'))

        flash(mensaje, 'danger')

    return render_template('auth/register.html')


@auth_bp.route('/test')
def test():
    return render_template('test.html')


# ⭐⭐ NUEVA RUTA: ESTADO DE CUENTA ⭐⭐
@auth_bp.route('/estado-cuenta')
@login_required
@acceso_permitido  # ← NUEVA LÍNEA
def estado_cuenta():
    """Muestra el estado de la cuenta al usuario"""
    # Calcular días transcurridos desde el registro
    fecha_registro = getattr(current_user, 'fecha_registro', datetime.utcnow())
    dias_transcurridos = (datetime.utcnow() - fecha_registro).days

    # Obtener días de prueba (por defecto 15 si no existe)
    dias_prueba = getattr(current_user, 'dias_prueba', 15)
    dias_restantes = max(0, dias_prueba - dias_transcurridos)

    # Verificar si está aprobado
    is_approved = getattr(current_user, 'is_approved', False)

    return render_template('auth/estado_cuenta.html',
                           dias_restantes=dias_restantes,
                           is_approved=is_approved)
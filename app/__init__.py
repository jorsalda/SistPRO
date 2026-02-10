from flask import Flask, redirect, url_for
import os
from flask_login import current_user
from .extensions import db, login_manager
from flask_migrate import Migrate


def create_app():
    # ✅ Configurar rutas absolutas para static_folder
    base_dir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, '..', 'static')

    app = Flask(__name__,
                template_folder="templates",
                static_folder=static_dir,
                static_url_path='/static')

    app.config.from_object('config.Config')

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)

    # ✅ FIX CRÍTICO: Verificar y crear/arreglar columna 'nombre' si no existe
    with app.app_context():
        try:
            # 1. Agregar columna si no existe
            db.session.execute("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS nombre VARCHAR(100)")
            # 2. Hacerla nullable
            db.session.execute("ALTER TABLE usuarios ALTER COLUMN nombre DROP NOT NULL")
            db.session.commit()
            print("✅ Columna 'nombre' verificada/arreglada en la base de datos")
        except Exception as e:
            db.session.rollback()
            print(f"ℹ️ Nota: {e}")

    # ⭐⭐ IMPORTANTE: Importar modelos AQUÍ para registrarlos una sola vez
    from .models.usuario import Usuario
    from .models.colegio import Colegio
    from .models.docente import Docente
    from .models.permiso import Permiso

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.permiso_routes import permiso_bp
    from .routes.docente_routes import docente_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(permiso_bp)
    app.register_blueprint(docente_bp)

    # Ruta raíz
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("permiso.listado"))
        return redirect(url_for("auth.login"))

    # Crear tablas (para desarrollo)
    with app.app_context():
        db.create_all()

    return app
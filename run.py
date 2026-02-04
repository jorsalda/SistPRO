# run.py
import os
import sys
import traceback
from flask import Flask

from config import Config
from app.extensions import db, login_manager
from app.models.usuario import Usuario
from app.routes.auth_routes import auth_bp
from app.routes.permiso_routes import permiso_bp
from app.routes.docente_routes import docente_bp


def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, 'app', 'templates')

    app = Flask(__name__, template_folder=template_path)

    try:
        app.config.from_object(Config)

        db.init_app(app)
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return Usuario.query.get(int(user_id))

        app.register_blueprint(auth_bp)
        app.register_blueprint(permiso_bp)
        app.register_blueprint(docente_bp)

        with app.app_context():
            db.create_all()
            print("✅ Tablas creadas/verificadas")

        return app

    except Exception as e:
        print(f"❌ ERROR AL INICIAR LA APP: {e}")
        traceback.print_exc()
        sys.exit(1)


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

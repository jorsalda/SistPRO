import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_super_segura')

    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        SQLALCHEMY_DATABASE_URI = database_url
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }
    else:
        SQLALCHEMY_DATABASE_URI = (
            "postgresql+psycopg2://postgres:jes8026@localhost:5432/permisos"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔹 Configuración de Email (Flask-Mail)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'jorgesaldarriaga3544@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # 🔹 CONFIGURACIÓN DINÁMICA: Local vs Producción ✅
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = (FLASK_ENV == 'development')

    # Cookies: Secure solo en producción (HTTPS)
    SESSION_COOKIE_SECURE = (FLASK_ENV == 'production')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PREFERRED_URL_SCHEME = 'https' if FLASK_ENV == 'production' else 'http'
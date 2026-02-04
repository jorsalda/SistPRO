# config.py
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
            "pool_pre_ping": True,  # ✅ Verifica conexiones antes de usarlas
            "pool_recycle": 300,  # ✅ Recicla conexiones cada 5 minutos (evita SSL corrupto)
            "connect_args": {
                "sslmode": "require"  # ✅ Requiere SSL (obligatorio en Render)
            }
        }
    else:
        SQLALCHEMY_DATABASE_URI = (
            "postgresql+psycopg2://postgres:jes8026@localhost:5432/permisos"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
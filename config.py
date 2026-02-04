# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_super_segura')

    # Base de datos (Render o local)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Fix para URLs antiguas tipo postgres://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            'postgres://', 'postgresql://', 1
        )

    # Fallback para desarrollo local
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = (
            'postgresql+psycopg2://postgres:jes8026@localhost:5432/permisos'
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

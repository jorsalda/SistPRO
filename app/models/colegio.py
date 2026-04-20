from app.extensions import db
from datetime import datetime


class Colegio(db.Model):
    __tablename__ = "colegios"
    __table_args__ = {'extend_existing': True}

    # --------------------
    # Columnas principales
    # --------------------
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    # ✅ Columnas según tu DDL
    codigo_acceso = db.Column(db.String(20), unique=True, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    en_prueba = db.Column(db.Boolean, default=True)
    fecha_expiracion = db.Column(db.DateTime, nullable=True)

    # --------------------
    # Relaciones
    # --------------------
    # ✅ Relación bidireccional con Usuario (CORREGIDA)
    usuarios = db.relationship("Usuario", back_populates='colegio', lazy=True)

    # ⚠️ Relación con Docente: SIN back_populates para evitar error
    # (Si necesitas acceder a colegio desde docente, deberás agregarlo en docente.py después)
    docentes = db.relationship("Docente", lazy=True)

    # --------------------
    # Representación
    # --------------------
    def __repr__(self):
        return f'<Colegio {self.nombre}>'
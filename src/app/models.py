from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nit = db.Column(db.String, unique=True, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, default="PENDIENTE")
    datos = db.Column(db.JSON, nullable=True)

    def as_dict(self):
        empresa_dict = {
            "id": self.id,
            "nit": self.nit,
            "nombre": self.nombre,
            "estado": self.estado,
        }
        # Solo incluir "datos" si realmente existe
        if self.datos is not None and self.datos != {}: 
            empresa_dict["datos"] = self.datos
        return empresa_dict

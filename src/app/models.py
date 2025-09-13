from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nit = db.Column(db.String, unique=True, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, default="PENDIENTE")
    datos = db.Column(db.JSON)

    def as_dict(self):
        return {
            "id": self.id,
            "nit": self.nit,
            "nombre": self.nombre,
            "estado": self.estado,
            "datos": self.datos,
        }
from flask import Flask
from flasgger import Swagger
from .models import db

def create_app():
    app = Flask(__name__)
    # SOLO ESTA LÍNEA CAMBIA: lee la base de datos de la variable de ambiente si existe
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///empresas.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SWAGGER"] = {"title": "API RPA Empresas", "uiversion": 3}
    db.init_app(app)
    Swagger(app)
    from .routes import bp as api_bp
    app.register_blueprint(api_bp)
    return app
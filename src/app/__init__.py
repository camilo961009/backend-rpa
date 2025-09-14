import os
from flask import Flask, jsonify
from flasgger import Swagger
from .models import db
from .routes import bp as api_bp

def create_app():
    app = Flask(__name__)

    # --- CONFIG DB ---
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Usa la BD de Render si está configurada, si no usa SQLite local
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        sqlite_path = os.path.join(BASE_DIR, "empresas.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqlite_path}"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SWAGGER"] = {"title": "API RPA Empresas", "uiversion": 3}

    db.init_app(app)
    Swagger(app)

    # 👇 Aquí garantizamos que las tablas se creen si no existen
    with app.app_context():
        db.create_all()

    app.register_blueprint(api_bp)

    # 👇 Capturar errores para verlos en Render
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception("Unhandled Exception:")
        return jsonify({"error": "Internal Server Error"}), 500

    return app

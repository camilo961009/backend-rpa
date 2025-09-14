import os
from flask import Flask, jsonify
from .models import db
from .routes import bp

def create_app():
    app = Flask(__name__)

    # --- CONFIG DB ---
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        # si no hay DATABASE_URL (local o Render sin postgres)
        sqlite_path = os.path.join(BASE_DIR, "empresas.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqlite_path}"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(bp)

    # capturar errores para que aparezcan en logs de Render
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception("Unhandled Exception:")
        return jsonify({"error": "Internal Server Error"}), 500

    return app

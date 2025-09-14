from flask import Blueprint, request, jsonify
from .models import db, Empresa

bp = Blueprint("api", __name__)

def is_valid_nit(nit):
    """Valida que el NIT sea numérico y de longitud adecuada (ej: 6-15 caracteres)."""
    return isinstance(nit, str) and nit.isdigit() and 6 <= len(nit) <= 15

def is_valid_nombre(nombre):
    """Valida que el nombre sea una cadena no vacía y sin solo espacios."""
    return isinstance(nombre, str) and nombre.strip() != ""

def is_valid_estado(estado):
    """Valida que el estado sea uno permitido."""
    return estado in ["PENDIENTE", "PROCESADO", "ERROR"]
@bp.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "API RPA Empresas funcionando 🚀",
        "endpoints": [
            {"path": "/process-data", "method": "POST"},
            {"path": "/update-status", "method": "POST"},
            {"path": "/empresas", "method": "GET"},
            {"path": "/empresa/<nit>", "method": "GET"},
            {"path": "/empresa/<nit>", "method": "DELETE"}
        ]
    }), 200

@bp.route("/process-data", methods=["POST"])
def process_data():
    """
    Procesa y almacena datos de una empresa.
    ---
    post:
      description: Almacena una nueva empresa si el NIT no existe.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                nit: {type: string}
                nombre: {type: string}
                datos: {type: object}
      responses:
        200: {description: Empresa almacenada correctamente}
        400: {description: Error en la petición}
    """
    data = request.get_json()
    nit = data.get("nit")
    nombre = data.get("nombre")

    # Validaciones básicas
    if not nit or not nombre:
        return jsonify({"error": "Los campos 'nit' y 'nombre' son obligatorios"}), 400

    # Eliminar "datos" si viene vacío
    if "datos" in data and not data["datos"]:
        data.pop("datos")

    # Capturar otros campos diferentes a nit/nombre
    otros_datos = data.get("datos")
    if not otros_datos:
        otros_datos = None

    empresa = Empresa(
        nit=nit,
        nombre=nombre,
        datos=otros_datos  #  nunca guarda {}
    )

    db.session.add(empresa)
    db.session.commit()

    return jsonify({
        "message": "Empresa almacenada correctamente",
        "empresa": empresa.as_dict()
    }), 201

@bp.route('/update-status', methods=['POST'])
def update_status():
    """
    Actualiza el estado de una empresa según su NIT.
    ---
    post:
      description: Cambia el estado de una empresa existente.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                nit: {type: string}
                estado: {type: string}
      responses:
        200: {description: Estado actualizado correctamente}
        404: {description: Empresa no encontrada}
        400: {description: Petición inválida}
    """
    data = request.get_json()
    nit = data.get("nit")
    nuevo_estado = data.get("estado")

    # Validaciones avanzadas
    if not is_valid_nit(nit):
        return jsonify({"error": "NIT inválido. Debe ser numérico y de 6-15 dígitos."}), 400
    if not is_valid_estado(nuevo_estado):
        return jsonify({"error": "Estado inválido. Opciones válidas: PENDIENTE, PROCESADO, ERROR."}), 400

    empresa = Empresa.query.filter_by(nit=nit).first()
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    empresa.estado = nuevo_estado
    db.session.commit()
    return jsonify({"message": "Estado actualizado correctamente", "empresa": empresa.as_dict()}), 200

@bp.route('/empresas', methods=['GET'])
def listar_empresas():
    """
    Lista todas las empresas registradas.
    ---
    get:
      description: Devuelve una lista con todas las empresas almacenadas.
      responses:
        200:
          description: Lista de empresas
          content:
            application/json:
              schema:
                type: object
                properties:
                  empresas:
                    type: array
                    items:
                      type: object
    """
    empresas = Empresa.query.all()
    return jsonify({"empresas": [e.as_dict() for e in empresas]}), 200
@bp.route('/empresa/<nit>', methods=['GET'])
def consultar_empresa(nit):
    """
    Consulta una empresa por su NIT.
    ---
    get:
      description: Devuelve los datos de una empresa específica por su NIT.
      parameters:
        - in: path
          name: nit
          schema:
            type: string
          required: true
          description: NIT de la empresa a consultar
      responses:
        200:
          description: Empresa encontrada
          content:
            application/json:
              schema:
                type: object
                properties:
                  empresa:
                    type: object
        404:
          description: Empresa no encontrada
    """
    empresa = Empresa.query.filter_by(nit=nit).first()
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    return jsonify({"empresa": empresa.as_dict()}), 200
@bp.route('/empresa/<nit>', methods=['DELETE'])
def eliminar_empresa(nit):
    """
    Elimina una empresa por su NIT.
    ---
    delete:
      description: Elimina la empresa cuyo NIT se indica.
      parameters:
        - in: path
          name: nit
          schema:
            type: string
          required: true
          description: NIT de la empresa a eliminar
      responses:
        200:
          description: Empresa eliminada correctamente
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
        404:
          description: Empresa no encontrada
    """
    empresa = Empresa.query.filter_by(nit=nit).first()
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    db.session.delete(empresa)
    db.session.commit()
    return jsonify({"message": "Empresa eliminada correctamente"}), 200



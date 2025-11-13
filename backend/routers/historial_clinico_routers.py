from flask import Blueprint, jsonify, request
from backend.services.historial_clinico_service import HistorialClinicoService

historial_bp = Blueprint("historial_clinico_bp", __name__,  url_prefix='/api/historial')
service = HistorialClinicoService()


# -----------------------------------
# GET /api/historial_clinico
# -----------------------------------
@historial_bp.route("/", methods=["GET"])
def listar_historiales():
    historiales = service.get_all()
    data = historiales
    return jsonify(data), 200

# -----------------------------------
# GET /api/historial_clinico/<id>
# -----------------------------------
@historial_bp.route("/<int:historial_id>", methods=["GET"])
def obtener_historial(historial_id):
    historial = service.get_by_id(historial_id)
    if not historial:
        return jsonify({"error": "Historial no encontrado"}), 404
    return jsonify(historial), 200


# -----------------------------------
# POST /api/historial_clinico
# -----------------------------------
@historial_bp.route("/", methods=["POST"])
def crear_historial():
    data = request.json
    nuevo_historial = service.create(data)
    if not nuevo_historial:
        return jsonify({"error": "No se pudo crear el historial"}), 400
    return jsonify(nuevo_historial), 201


# -----------------------------------
# PUT /api/historial_clinico/<id>
# -----------------------------------
@historial_bp.route("/<int:historial_id>", methods=["PUT"])
def actualizar_historial(historial_id):
    data = request.json
    historial_actualizado = service.update(historial_id, data)
    if not historial_actualizado:
        return jsonify({"error": "No se pudo actualizar el historial"}), 400
    return jsonify(historial_actualizado), 200

# -----------------------------------
# DELETE /api/historial_clinico/<id>
# -----------------------------------
@historial_bp.route("/<int:historial_id>", methods=["DELETE"])
def eliminar_historial(historial_id):
    eliminado = service.delete(historial_id)
    if not eliminado:
        return jsonify({"error": "No se pudo eliminar el historial"}), 400
    return jsonify({"mensaje": "Historial eliminado correctamente"}), 200

# -----------------------------------
# GET /api/historiales_clinicos/paciente/<id_paciente>
# -----------------------------------
@historial_bp.route("/paciente/<int:id_paciente>", methods=["GET"])
def obtener_por_paciente(id_paciente):
    try:
        historial = service.get_by_paciente(id_paciente)
        if not historial:
            return jsonify({"success": False, "error": "Historial no encontrado para el paciente"}), 404
        return jsonify({"success": True, "data": historial}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
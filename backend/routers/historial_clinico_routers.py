from flask import Blueprint, jsonify, request
from services.historial_clinico_service import HistorialClinicoService

historial_bp = Blueprint("historial_clinico_bp", __name__)
service = HistorialClinicoService()


@historial_bp.route("/historial", methods=["GET"])
def listar_historiales():
    historiales = service.get_all()
    data = [h.__dict__ for h in historiales]
    return jsonify(data), 200


@historial_bp.route("/historial/<int:historial_id>", methods=["GET"])
def obtener_historial(historial_id):
    historial = service.get_by_id(historial_id)
    if not historial:
        return jsonify({"error": "Historial no encontrado"}), 404
    return jsonify(historial.__dict__), 200


@historial_bp.route("/historial", methods=["POST"])
def crear_historial():
    data = request.json
    nuevo_historial = service.create(data)
    if not nuevo_historial:
        return jsonify({"error": "No se pudo crear el historial"}), 400
    return jsonify(nuevo_historial.__dict__), 201


@historial_bp.route("/historial/<int:historial_id>", methods=["PUT"])
def actualizar_historial(historial_id):
    data = request.json
    historial_actualizado = service.update(historial_id, data)
    if not historial_actualizado:
        return jsonify({"error": "No se pudo actualizar el historial"}), 400
    return jsonify(historial_actualizado.__dict__), 200


@historial_bp.route("/historial/<int:historial_id>", methods=["DELETE"])
def eliminar_historial(historial_id):
    eliminado = service.delete(historial_id)
    if not eliminado:
        return jsonify({"error": "No se pudo eliminar el historial"}), 400
    return jsonify({"mensaje": "Historial eliminado correctamente"}), 200

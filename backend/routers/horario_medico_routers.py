from flask import Blueprint, request, jsonify
from services.horario_medico_service import HorarioMedicoService

horario_medico_bp = Blueprint("horario_medico_bp", __name__)
service = HorarioMedicoService()

@horario_medico_bp.route("/", methods=["POST"])
def crear_horario():
    data = request.json
    horario = service.crear_horario(data)
    if horario:
        return jsonify({"mensaje": "Horario creado correctamente", "horario": horario.__dict__}), 201
    return jsonify({"error": "No se pudo crear el horario"}), 400

@horario_medico_bp.route("/", methods=["GET"])
def obtener_todos():
    horarios = service.obtener_todos()
    return jsonify([h.__dict__ for h in horarios]), 200

@horario_medico_bp.route("/<int:horario_id>", methods=["GET"])
def obtener_por_id(horario_id):
    horario = service.obtener_por_id(horario_id)
    if horario:
        return jsonify(horario.__dict__), 200
    return jsonify({"error": "Horario no encontrado"}), 404

@horario_medico_bp.route("/medico/<int:id_medico>", methods=["GET"])
def obtener_por_medico(id_medico):
    horarios = service.obtener_por_medico(id_medico)
    return jsonify([h.__dict__ for h in horarios]), 200

@horario_medico_bp.route("/<int:horario_id>", methods=["PUT"])
def modificar(horario_id):
    data = request.json
    horario = service.modificar(horario_id, data)
    if horario:
        return jsonify({"mensaje": "Horario actualizado", "horario": horario.__dict__}), 200
    return jsonify({"error": "No se pudo actualizar el horario"}), 400

@horario_medico_bp.route("/<int:horario_id>", methods=["DELETE"])
def eliminar(horario_id):
    success = service.eliminar(horario_id)
    if success:
        return jsonify({"mensaje": "Horario eliminado correctamente"}), 200
    return jsonify({"error": "No se pudo eliminar el horario"}), 400

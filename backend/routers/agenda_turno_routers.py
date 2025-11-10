from flask import Blueprint, request, jsonify
from services.agenda_turno_service import AgendaTurnoService

agenda_turno_bp = Blueprint("agenda_turno_bp", __name__)
service = AgendaTurnoService()

@agenda_turno_bp.route("/", methods=["POST"])
def crear_agenda():
    data = request.json
    agenda = service.create(data)
    if agenda:
        return jsonify({"mensaje": "✅ Turno creado correctamente", "agenda": agenda.__dict__}), 201
    return jsonify({"error": "No se pudo crear el turno"}), 400

@agenda_turno_bp.route("/", methods=["GET"])
def obtener_todos():
    agendas = service.get_all()
    return jsonify([a.__dict__ for a in agendas]), 200

@agenda_turno_bp.route("/<int:agenda_id>", methods=["GET"])
def obtener_por_id(agenda_id):
    agenda = service.get_by_id(agenda_id)
    if agenda:
        return jsonify(agenda.__dict__), 200
    return jsonify({"error": "Turno no encontrado"}), 404

@agenda_turno_bp.route("/<int:agenda_id>", methods=["PUT"])
def modificar(agenda_id):
    data = request.json
    agenda = service.update(agenda_id, data)
    if agenda:
        return jsonify({"mensaje": "Turno actualizado", "agenda": agenda.__dict__}), 200
    return jsonify({"error": "No se pudo actualizar el turno"}), 400

@agenda_turno_bp.route("/<int:agenda_id>", methods=["DELETE"])
def eliminar(agenda_id):
    success = service.delete(agenda_id)
    if success:
        return jsonify({"mensaje": "Turno eliminado correctamente"}), 200
    return jsonify({"error": "No se pudo eliminar el turno"}), 400

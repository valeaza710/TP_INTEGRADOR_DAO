from flask import Blueprint, request, jsonify
rom backend.services.agenda_turno_service import AgendaTurnoService

turnos_bp = Blueprint('turnos', __name__, url_prefix='/api/turnos')
service = AgendaTurnoService()

@turnos_bp.route("/", methods=["GET"])
def listar_turnos():
    return jsonify(service.get_all()), 200

@turnos_bp.route("/", methods=["POST"])
def crear_turno():
    data = request.get_json()
    nuevo = service.create(data)
    return jsonify(nuevo), 201

@turnos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_turno(id):
    ok = service.delete(id)
    return ({"success": True}, 200) if ok else ({"error": "No existe"}, 404)

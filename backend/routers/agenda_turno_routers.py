from flask import Blueprint, request, jsonify
from backend.services.agenda_turno_service import AgendaTurnoService

agenda_turno_bp = Blueprint("agenda_turno_bp", __name__, url_prefix="/api/agenda")
service = AgendaTurnoService()

# -----------------------------------
# POST /api/agenda
# -----------------------------------
@agenda_turno_bp.route("/", methods=["POST"])
def crear_agenda():
    data = request.get_json()
    try:
        agenda = service.create(data)
        return jsonify(agenda), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -----------------------------------
# GET /api/agenda
# -----------------------------------
@agenda_turno_bp.route("/", methods=["GET"])
def obtener_todos():
    agendas = service.get_all()
    return jsonify(agendas), 200

# -----------------------------------
# GET /api/agenda/<id>
# -----------------------------------
@agenda_turno_bp.route("/<int:agenda_id>", methods=["GET"])
def obtener_por_id(agenda_id):
    agenda = service.get_by_id(agenda_id)
    if agenda:
        return jsonify(agenda), 200
    return jsonify({"error": "Turno no encontrado"}), 404

# -----------------------------------
# PUT /api/agenda/<id>
# -----------------------------------
@agenda_turno_bp.route("/<int:agenda_id>", methods=["PUT"])
def modificar(agenda_id):
    data = request.get_json()
    agenda = service.update(agenda_id, data)
    if agenda:
        return jsonify(agenda), 200
    return jsonify({"error": "No se pudo actualizar el turno"}), 400

# -----------------------------------
# DELETE /api/agenda/<id>
# -----------------------------------
@agenda_turno_bp.route("/<int:agenda_id>", methods=["DELETE"])
def eliminar(agenda_id):
    success = service.delete(agenda_id)
    if success:
        return jsonify({"mensaje": "Turno eliminado correctamente"}), 200
    return jsonify({"error": "No se pudo eliminar el turno"}), 400


# -----------------------------------
# GET /api/agenda/medico/<id_medico>
# -----------------------------------
@agenda_turno_bp.route("/medico/<int:id_medico>", methods=["GET"])
def obtener_turnos_por_medico(id_medico):
    """
    Devuelve los turnos de un médico, excluyendo estados 1, 4 y 5.
    """
    try:
        turnos = service.get_by_medico(id_medico)
        return jsonify({
            "success": True,
            "data": turnos,
            "count": len(turnos)
        }), 200

    except Exception as e:
        print(f"❌ Error en obtener_turnos_por_medico: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------------
# GET /api/agenda/medico/<id_medico>/historial
# -----------------------------------
@agenda_turno_bp.route("/medico/<int:id_medico>/historial", methods=["GET"])
def obtener_historial_medico(id_medico):
    """
    Devuelve los turnos atendidos (estado = 3) de un médico.
    """
    try:
        turnos = service.get_historial_by_medico(id_medico)
        return jsonify({
            "success": True,
            "data": turnos,
            "count": len(turnos)
        }), 200
    except Exception as e:
        print(f"❌ Error en obtener_historial_medico: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# GET /api/agenda/medico/<id_medico>/hoy
# -----------------------------------
@agenda_turno_bp.route("/medico/<int:id_medico>/hoy", methods=["GET"])
def obtener_turnos_hoy_medico(id_medico):
    """
    Devuelve los turnos del día actual de un médico.
    """
    try:
        print(f"📩 [ROUTER] Solicitando turnos de hoy para médico ID={id_medico}")
        turnos = service.get_turnos_hoy_by_medico(id_medico)
        return jsonify({
            "success": True,
            "data": turnos,
            "count": len(turnos)
        }), 200

    except Exception as e:
        print(f"❌ Error en obtener_turnos_hoy_medico (router): {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# GET /api/agenda/detalles
@agenda_turno_bp.route("/detalles", methods=["GET"])
def obtener_turnos_detalles():
    try:
        turnos = service.obtener_todos_los_turnos()
        return jsonify(turnos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------------
# GET /api/agenda/paciente/<int:id_paciente>
# -----------------------------------
@agenda_turno_bp.route("/paciente/<int:id_paciente>", methods=["GET"])
def obtener_por_paciente(id_paciente):
    try:
        turnos = service.get_by_paciente(id_paciente)
        return jsonify({
            "success": True,
            "count": len(turnos),
            "data": turnos
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

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
    agenda = service.create(data)
    
    if not agenda:
        return jsonify({"error": "No se pudo crear el turno"}), 400
    
    return jsonify({
        "mensaje": "✅ Turno creado correctamente",
        "agenda": agenda.to_dict()
    }), 201


# -----------------------------------
# GET /api/agenda
# -----------------------------------
@agenda_turno_bp.route("/", methods=["GET"])
def obtener_todos():
    agendas = service.get_all()
    return jsonify([a.to_dict() for a in agendas]), 200


# -----------------------------------
# GET /api/agenda/<id>
# -----------------------------------
@agenda_turno_bp.route("/<int:agenda_id>", methods=["GET"])
def obtener_por_id(agenda_id):
    agenda = service.get_by_id(agenda_id)
    
    if not agenda:
        return jsonify({"error": "Turno no encontrado"}), 404
    
    return jsonify(agenda.to_dict()), 200


# -----------------------------------
# PUT /api/agenda/<id>
# -----------------------------------
@agenda_turno_bp.route("/<int:agenda_id>", methods=["PUT"])
def modificar(agenda_id):
    data = request.get_json()
    agenda = service.update(agenda_id, data)

    if not agenda:
        return jsonify({"error": "No se pudo actualizar el turno"}), 404

    return jsonify({
        "mensaje": "Turno actualizado",
        "agenda": agenda.to_dict()
    }), 200


# -----------------------------------
# DELETE /api/agenda/<id>
# -----------------------------------
@agenda_turno_bp.route("/<int:agenda_id>", methods=["DELETE"])
def eliminar(agenda_id):
    success = service.delete(agenda_id)
    
    if success is None:
        return jsonify({"error": "Turno no encontrado"}), 404
    
    if success is False:
        return jsonify({"error": "No se pudo eliminar el turno"}), 500

    return jsonify({"mensaje": "Turno eliminado correctamente"}), 200


# -----------------------------------
# GET /api/agenda/medico/<id_medico>
# -----------------------------------
@agenda_turno_bp.route("/medico/<int:id_medico>", methods=["GET"])
def obtener_turnos_por_medico(id_medico):
    try:
        turnos = service.get_by_medico(id_medico)
        
        if not turnos:
            return jsonify({"mensaje": "No se encontraron turnos para este médico"}), 404
        
        return jsonify([t.to_dict() for t in turnos]), 200
    
    except Exception as e:
        print(f"❌ Error en /api/agenda/medico/{id_medico}: {e}")
        return jsonify({"error": "Error al obtener los turnos del médico"}), 500

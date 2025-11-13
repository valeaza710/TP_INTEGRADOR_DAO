# backend/routers/turno_routers.py
from flask import Blueprint, request, jsonify
from backend.services.turno_service import TurnoService
turnos_bp = Blueprint('turnos', __name__, url_prefix='/api/turnos')
service = TurnoService()

# ---------------------------------------------
# GET: listar todos los turnos
# ---------------------------------------------
@turnos_bp.route('/', methods=['GET'])
def listar_turnos():
    try:
        turnos = service.get_all()
        return jsonify({
            "success": True,
            "data": turnos
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ---------------------------------------------
# POST: crear un nuevo turno
# ---------------------------------------------
@turnos_bp.route('/', methods=['POST'])
def crear_turno():
    try:
        data = request.get_json()
        nuevo = service.create(data)

        # Si AgendaTurnoService devolvió una tupla (jsonify, status)
        if isinstance(nuevo, tuple):
            return nuevo

        return jsonify({
            "success": True,
            "data": nuevo
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# ---------------------------------------------
# DELETE: eliminar turno por ID
# ---------------------------------------------
@turnos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_turno(id):
    try:
        result = service.delete(id)
        if result:
            return jsonify({
                "success": True,
                "message": "Turno eliminado correctamente"
            }), 200
        return jsonify({
            "success": False,
            "error": "Turno no encontrado"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@turnos_bp.route('/slots', methods=['POST'])
def get_slots():
    """
    Espera JSON con:
    {
        "specialty": "Cardiología",
        "doctor": "Dr. Juan Pérez",
        "date": "2025-11-12"
    }
    Devuelve lista de horarios disponibles con id_horario_medico
    """
    data = request.get_json()
    specialty = data.get("specialty")
    doctor_name = data.get("doctor")
    date = data.get("date")

    # Usamos repo para filtrar horarios libres
    turnos_service = TurnoService()
    slots = turnos_service.get_available_slots(specialty, doctor_name, date)

    # slots = [{ "id_horario_medico": 2, "doctor": "Dr. Juan Pérez", "time": "15:00", "location": "Consultorio 3" }, ...]
    return jsonify(slots), 200

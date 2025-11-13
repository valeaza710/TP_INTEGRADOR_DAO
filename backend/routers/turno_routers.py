# backend/routers/turno_routers.py
from flask import Blueprint, request, jsonify
from backend.services.turno_service import TurnoService

turnos_bp = Blueprint('turnos', __name__, url_prefix='/api/turnos')
turnos_service = TurnoService()


# ---------------------------------------------
# GET: listar todos los turnos
# ---------------------------------------------
@turnos_bp.route('/', methods=['GET'])
def listar_turnos():
    try:
        turnos = turnos_service.get_all()
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
        nuevo = turnos_service.create(data)
        
        # Si la respuesta es una tupla (es decir, el error de jsonify), la devolvemos
        if isinstance(nuevo, tuple):
            return nuevo # Devuelve (response, status_code)
        
        # Si es exitoso, devolvemos el objeto serializado
        return jsonify({"message": "Turno creado/reservado exitosamente", "turno": nuevo}), 201

    except Exception as e:
        print(f"❌ Error al intentar crear turno: {e}")
        return jsonify({"error": "Error interno del servidor al crear turno"}), 500

# ---------------------------------------------
# DELETE: eliminar turno por ID
# ---------------------------------------------
@turnos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_turno(id):
    try:
        result = turnos_service.delete(id)
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

@turnos_bp.route('/slots', methods=['GET', 'POST'])
def get_slots():
    if request.method == 'GET':
        return jsonify({"message": "Usa POST para filtrar por especialidad y fecha"}), 200

    data = request.get_json()
    specialty = data.get("specialty")
    doctor_name = data.get("doctor")
    date = data.get("date")

    #turnos_service = TurnoService()
    slots = turnos_service.get_available_slots(specialty, doctor_name, date)

    return jsonify(slots), 200


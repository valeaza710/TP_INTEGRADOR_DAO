from flask import Blueprint, request, jsonify
from services.estado_turno_service import EstadoTurnoService

# Crear blueprint
estado_turnos_bp = Blueprint("estado_turnos", __name__, url_prefix="/api/estado_turnos")

# Instanciar el servicio
estado_turno_service = EstadoTurnoService()

# Listar todos
@estado_turnos_bp.route("/", methods=["GET"])
def listar_estados():
    try:
        estados = estado_turno_service.get_all()
        return jsonify({
            "success": True,
            "data": [e.__dict__ for e in estados],
            "count": len(estados)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Obtener uno por ID
@estado_turnos_bp.route("/<int:id>", methods=["GET"])
def obtener_estado(id):
    try:
        estado = estado_turno_service.get_by_id(id)
        if not estado:
            return jsonify({"success": False, "error": "Estado no encontrado"}), 404
        return jsonify({"success": True, "data": estado.__dict__}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Crear uno nuevo
@estado_turnos_bp.route("/", methods=["POST"])
def crear_estado():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        nuevo = estado_turno_service.create(data)
        return jsonify({
            "success": True,
            "data": nuevo.__dict__,
            "message": "Estado de turno creado exitosamente"
        }), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Modificar uno existente
@estado_turnos_bp.route("/<int:id>", methods=["PUT"])
def actualizar_estado(id):
    try:
        data = request.get_json()
        actualizado = estado_turno_service.update(id, data)
        if not actualizado:
            return jsonify({"success": False, "error": "Estado no encontrado"}), 404

        return jsonify({
            "success": True,
            "data": actualizado.__dict__,
            "message": "Estado actualizado exitosamente"
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Eliminar uno
@estado_turnos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_estado(id):
    try:
        eliminado = estado_turno_service.delete(id)
        if eliminado is None:
            return jsonify({"success": False, "error": "Estado no encontrado"}), 404
        if not eliminado:
            return jsonify({"success": False, "error": "No se pudo eliminar el estado"}), 500

        return jsonify({"success": True, "message": "Estado eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


__all__ = ["estado_turnos_bp"]

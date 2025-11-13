from flask import Blueprint, request, jsonify
from backend.services.historial_enfermedad_service import HistorialEnfermedadService

# Blueprint
historial_enfermedad_bp = Blueprint('historial_enfermedad_bp', __name__, url_prefix='/api/historiales_enfermedad')

# Instancia del service
historial_service = HistorialEnfermedadService()


# -----------------------------------
# GET /api/historiales_enfermedad
# -----------------------------------
@historial_enfermedad_bp.route('/', methods=['GET'])
def listar_historiales_enfermedad():
    try:
        historiales = historial_service.get_all()
        return jsonify({
            "success": True,
            "data": historiales,
            "count": len(historiales)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# GET /api/historiales_enfermedad/<id>
# -----------------------------------
@historial_enfermedad_bp.route('/<int:id>', methods=['GET'])
def obtener_historial_enfermedad(id):
    try:
        historial = historial_service.get_by_id(id)
        if not historial:
            return jsonify({"success": False, "error": "Historial de enfermedad no encontrado"}), 404

        return jsonify({"success": True, "data": historial}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# GET /api/historiales_enfermedad/paciente/<id_paciente>
# -----------------------------------
@historial_enfermedad_bp.route('/paciente/<int:id_paciente>', methods=['GET'])
def obtener_historiales_por_paciente(id_paciente):
    """
    Devuelve todos los historiales de enfermedad vinculados a un paciente específico
    """
    try:
        historiales = historial_service.get_by_paciente(id_paciente)
        if not historiales:
            return jsonify({"success": True, "data": [], "message": "No hay registros para este paciente"}), 200

        return jsonify({
            "success": True,
            "data": historiales,
            "count": len(historiales)
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# POST /api/historiales_enfermedad
# -----------------------------------
@historial_enfermedad_bp.route('/', methods=['POST'])
def crear_historial_enfermedad():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        nuevo = historial_service.create(data)
        return jsonify({
            "success": True,
            "data": nuevo,
            "message": "Historial de enfermedad creado exitosamente"
        }), 201

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# PUT /api/historiales_enfermedad/<id>
# -----------------------------------
@historial_enfermedad_bp.route('/<int:id>', methods=['PUT'])
def actualizar_historial_enfermedad(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        actualizado = historial_service.update(id, data)
        if not actualizado:
            return jsonify({"success": False, "error": "Historial de enfermedad no encontrado"}), 404

        return jsonify({
            "success": True,
            "data": actualizado,
            "message": "Historial de enfermedad actualizado exitosamente"
        }), 200

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# DELETE /api/historiales_enfermedad/<id>
# -----------------------------------
@historial_enfermedad_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_historial_enfermedad(id):
    try:
        eliminado = historial_service.delete(id)

        if eliminado is None:
            return jsonify({"success": False, "error": "Historial de enfermedad no encontrado"}), 404

        if not eliminado:
            return jsonify({"success": False, "error": "No se pudo eliminar el historial de enfermedad"}), 500

        return jsonify({"success": True, "message": "Historial de enfermedad eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

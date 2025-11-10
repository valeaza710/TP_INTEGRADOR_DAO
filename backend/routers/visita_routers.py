from flask import Blueprint, request, jsonify
from services.visita_service import VisitaService

visitas_bp = Blueprint('visitas', __name__, url_prefix='/api/visitas')

visita_service = VisitaService()

# -----------------------------------
# GET /api/visitas
# -----------------------------------
@visitas_bp.route('/', methods=['GET'])
def listar_visitas():
    try:
        visitas = visita_service.get_all()
        return jsonify({
            "success": True,
            "data": visitas,
            "count": len(visitas)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# GET /api/visitas/<id>
# -----------------------------------
@visitas_bp.route('/<int:id>', methods=['GET'])
def obtener_visita(id):
    try:
        visita = visita_service.get_by_id(id)
        if not visita:
            return jsonify({"success": False, "error": "Visita no encontrada"}), 404
        
        return jsonify({"success": True, "data": visita}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# POST /api/visitas
# -----------------------------------
@visitas_bp.route('/', methods=['POST'])
def crear_visita():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        nueva = visita_service.create(data)

        return jsonify({
            "success": True,
            "data": nueva,
            "message": "Visita creada exitosamente"
        }), 201

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# PUT /api/visitas/<id>
# -----------------------------------
@visitas_bp.route('/<int:id>', methods=['PUT'])
def actualizar_visita(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        actualizada = visita_service.update(id, data)

        if not actualizada:
            return jsonify({"success": False, "error": "Visita no encontrada"}), 404

        return jsonify({
            "success": True,
            "data": actualizada,
            "message": "Visita actualizada exitosamente"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# DELETE /api/visitas/<id>
# -----------------------------------
@visitas_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_visita(id):
    try:
        eliminado = visita_service.delete(id)

        if eliminado is None:
            return jsonify({
                "success": False,
                "error": "Visita no encontrada"
            }), 404

        if not eliminado:
            return jsonify({
                "success": False,
                "error": "No se pudo eliminar la visita"
            }), 500

        return jsonify({"success": True, "message": "Visita eliminada exitosamente"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

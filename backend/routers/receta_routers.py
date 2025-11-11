from flask import Blueprint, request, jsonify
from backend.services.receta_service import RecetaService

recetas_bp = Blueprint('recetas', __name__, url_prefix='/api/recetas')

receta_service = RecetaService()

# -----------------------------------
# GET /api/recetas
# -----------------------------------
@recetas_bp.route('/', methods=['GET'])
def listar_recetas():
    try:
        recetas = receta_service.get_all()
        return jsonify({
            "success": True,
            "data": recetas,
            "count": len(recetas)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------------
# GET /api/recetas/<id>
# -----------------------------------
@recetas_bp.route('/<int:id>', methods=['GET'])
def obtener_receta(id):
    try:
        receta = receta_service.get_by_id(id)
        if not receta:
            return jsonify({"success": False, "error": "Receta no encontrada"}), 404
        
        return jsonify({
            "success": True,
            "data": receta
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------------
# POST /api/recetas
# -----------------------------------
@recetas_bp.route('/', methods=['POST'])
def crear_receta():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400
        
        nueva = receta_service.create(data)

        return jsonify({
            "success": True,
            "data": nueva,
            "message": "Receta creada exitosamente"
        }), 201

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------------
# PUT /api/recetas/<id>
# -----------------------------------
@recetas_bp.route('/<int:id>', methods=['PUT'])
def actualizar_receta(id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400
        
        actualizada = receta_service.update(id, data)

        if not actualizada:
            return jsonify({"success": False, "error": "Receta no encontrada"}), 404
        
        return jsonify({
            "success": True,
            "data": actualizada,
            "message": "Receta actualizada exitosamente"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------------
# DELETE /api/recetas/<id>
# -----------------------------------
@recetas_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_receta(id):
    try:
        eliminado = receta_service.delete(id)
        
        if eliminado is None:
            return jsonify({
                "success": False,
                "error": "Receta no encontrada"
            }), 404
        
        if not eliminado:
            return jsonify({
                "success": False,
                "error": "No se pudo eliminar la receta"
            }), 500
        
        return jsonify({
            "success": True,
            "message": "Receta eliminada exitosamente"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# GET /api/recetas/paciente/<id_paciente>
# -----------------------------------
@recetas_bp.route("/paciente/<int:id_paciente>", methods=["GET"])
def recetas_por_paciente(id_paciente):
    try:
        recetas = RecetaService.get_by_paciente(id_paciente)
        return jsonify({"success": True, "data": recetas, "count": len(recetas)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
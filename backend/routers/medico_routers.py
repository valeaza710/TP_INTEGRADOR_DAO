from flask import Blueprint, request, jsonify
from backend.services.medico_service import MedicoService

medicos_bp = Blueprint('medicos', __name__, url_prefix='/api/medicos')

medico_service = MedicoService()

# -----------------------------------
# GET /api/medicos
# -----------------------------------
@medicos_bp.route('/', methods=['GET'])
def listar_medicos():
    try:
        medicos = medico_service.get_all()
        return jsonify({
            "success": True,
            "data": medicos,
            "count": len(medicos)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# GET /api/medicos/<id>
# -----------------------------------
@medicos_bp.route('/<int:id>', methods=['GET'])
def obtener_medico(id):
    try:
        medico = medico_service.get_by_id(id)
        if not medico:
            return jsonify({"success": False, "error": "Médico no encontrado"}), 404

        return jsonify({"success": True, "data": medico}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# POST /api/medicos
# -----------------------------------
@medicos_bp.route('/', methods=['POST'])
def crear_medico():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        nuevo = medico_service.create(data)
        return jsonify({
            "success": True,
            "data": nuevo,
            "message": "Médico creado exitosamente"
        }), 201

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# PUT /api/medicos/<id>
# -----------------------------------
@medicos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_medico(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        actualizado = medico_service.update(id, data)
        
        if not actualizado:
            return jsonify({"success": False, "error": "Médico no encontrado"}), 404

        return jsonify({
            "success": True,
            "data": actualizado,
            "message": "Médico actualizado exitosamente"
        }), 200

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# DELETE /api/medicos/<id>
# -----------------------------------
@medicos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_medico(id):
    try:
        eliminado = medico_service.delete(id)

        if eliminado is None:
            return jsonify({
                "success": False,
                "error": "Médico no encontrado"
            }), 404

        if not eliminado:
            return jsonify({
                "success": False,
                "error": "No se pudo eliminar el médico"
            }), 500

        return jsonify({"success": True, "message": "Médico eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
    

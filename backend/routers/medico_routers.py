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

@medicos_bp.route('/buscar', methods=['GET'])
def buscar_medicos():
    # 💡 Asumiendo que el JS envía 'nombre' o 'q'
    query_text = request.args.get('nombre') or request.args.get('q') 
    
    if not query_text:
        return jsonify({'success': False, 'error': 'Falta parámetro de búsqueda'}), 400
    
    try:
        # Llama al MedicoService.search
        resultados = medico_service.search(query_text)
        return jsonify({'success': True, 'data': resultados}), 200
    except Exception as e:
        print(f"ERROR EN BUSCAR MÉDICOS: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
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

# -----------------------------------
# GET /api/medicos/por_especialidad/<nombre>
# -----------------------------------
@medicos_bp.route('/por_especialidad/<string:nombre>', methods=['GET'])
def listar_por_especialidad(nombre):
    """
    Devuelve lista de médicos que tengan la especialidad indicada.
    Ejemplo: GET /api/medicos/por_especialidad/Cardiología
    """
    try:
        medicos = medico_service.get_by_especialidad(nombre)
        return jsonify({
            "success": True,
            "data": medicos,
            "count": len(medicos)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

#-----------------------------------------
#GET solo info basic
# ----------------------------------------
@medicos_bp.route('/basico', methods=['GET'])
def listar_medicos_basico():
    """GET /api/medicos/basico - Listar médicos con información básica"""
    try:
        medicos = medico_service.get_all_basic()
        return jsonify({
            'success': True,
            'data': medicos,
            'count': len(medicos)
        }), 200
    except Exception as e:
        print(f"Error en listar_medicos_basico: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

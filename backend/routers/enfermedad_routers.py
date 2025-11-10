from flask import Blueprint, request, jsonify
from services.enfermedad_service import EnfermedadService

enfermedades_bp = Blueprint('enfermedades', __name__, url_prefix='/api/enfermedades')
enfermedad_service = EnfermedadService()

# -----------------------------------
# GET /api/enfermedades
# -----------------------------------
@enfermedades_bp.route('/', methods=['GET'])
def listar_enfermedades():
    """GET /api/enfermedades - Listar todas las enfermedades"""
    try:
        enfermedades = enfermedad_service.get_all()
        return jsonify({'success': True, 'data': enfermedades, 'count': len(enfermedades)}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# -----------------------------------
# GET /api/enfermedades/<id>
# -----------------------------------
@enfermedades_bp.route('/<int:id>', methods=['GET'])
def obtener_enfermedad(id):
    """GET /api/enfermedades/:id - Obtener una enfermedad por ID"""
    try:
        enfermedad = enfermedad_service.get_by_id(id)
        if not enfermedad:
            return jsonify({'success': False, 'error': 'Enfermedad no encontrada'}), 404
        return jsonify({'success': True, 'data': enfermedad}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# -----------------------------------
# POST /api/enfermedades
# -----------------------------------
@enfermedades_bp.route('/', methods=['POST'])
def crear_enfermedad():
    """POST /api/enfermedades - Crear nueva enfermedad"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No se enviaron datos'}), 400

        nueva = enfermedad_service.create(data)
        return jsonify({'success': True, 'data': nueva, 'message': 'Enfermedad creada exitosamente'}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# -----------------------------------
# PUT /api/enfermedades/<id>
# -----------------------------------
@enfermedades_bp.route('/<int:id>', methods=['PUT'])
def actualizar_enfermedad(id):
    """PUT /api/enfermedades/:id - Actualizar enfermedad"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No se enviaron datos'}), 400

        actualizada = enfermedad_service.update(id, data)
        if not actualizada:
            return jsonify({'success': False, 'error': 'Enfermedad no encontrada'}), 404

        return jsonify({'success': True, 'data': actualizada, 'message': 'Enfermedad actualizada exitosamente'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# -----------------------------------
# DELETE /api/enfermedades/<id>
# -----------------------------------
@enfermedades_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_enfermedad(id):
    """DELETE /api/enfermedades/:id - Eliminar enfermedad"""
    try:
        eliminado = enfermedad_service.delete(id)
        if eliminado is None:
            return jsonify({'success': False, 'error': 'Enfermedad no encontrada'}), 404
        if not eliminado:
            return jsonify({'success': False, 'error': 'No se pudo eliminar la enfermedad'}), 500
        return jsonify({'success': True, 'message': 'Enfermedad eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# -----------------------------------
# GET /api/enfermedades/<nombre>
# -----------------------------------
@enfermedades_bp.route('/buscar', methods=['GET'])
def buscar_enfermedades_por_nombre():
    """GET /api/enfermedades/buscar?nombre=asma"""
    try:
        nombre = request.args.get('nombre', None)
        if not nombre:
            return jsonify({'success': False, 'error': 'Debe especificar un valor de búsqueda (nombre)'}), 400

        resultados = enfermedad_service.search_by_nombre(nombre)
        return jsonify({'success': True, 'data': resultados, 'count': len(resultados)}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

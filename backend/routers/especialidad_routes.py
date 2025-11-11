from flask import Blueprint, request, jsonify
from backend.services.especialidad_service import EspecialidadService

# Crear blueprint
especialidades_bp = Blueprint('especialidades', __name__, url_prefix='/api/especialidades')

# Instanciar servicio
especialidad_service = EspecialidadService()

# -----------------------------------
# GET /api/especialidades
# -----------------------------------
@especialidades_bp.route('/', methods=['GET'])
def listar_especialidades():
    """
    GET /api/especialidades
    Listar todas las especialidades
    """
    try:
        especialidades = especialidad_service.get_all()
        return jsonify({
            'success': True,
            'data': especialidades,
            'count': len(especialidades)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# -----------------------------------
# GET /api/especialidades/<id>
# -----------------------------------
@especialidades_bp.route('/<int:id>', methods=['GET'])
def obtener_especialidad(id):
    """
    GET /api/especialidades/:id
    Obtener una especialidad por ID
    """
    try:
        especialidad = especialidad_service.get_by_id(id)
        if not especialidad:
            return jsonify({
                'success': False,
                'error': 'Especialidad no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': especialidad
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# -----------------------------------
# POST /api/especialidades
# -----------------------------------
@especialidades_bp.route('/', methods=['POST'])
def crear_especialidad():
    """
    POST /api/especialidades
    Crear una nueva especialidad
    Body: { "nombre": "Cardiología" }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se enviaron datos'
            }), 400
        
        nueva = especialidad_service.create(data)
        return jsonify({
            'success': True,
            'data': nueva,
            'message': 'Especialidad creada exitosamente'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# -----------------------------------
# PUT /api/especialidades/<id>
# -----------------------------------
@especialidades_bp.route('/<int:id>', methods=['PUT'])
def actualizar_especialidad(id):
    """
    PUT /api/especialidades/:id
    Actualizar una especialidad
    Body: { "nombre": "Cardiología Pediátrica" }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se enviaron datos'
            }), 400
        
        actualizada = especialidad_service.update(id, data)
        
        if not actualizada:
            return jsonify({
                'success': False,
                'error': 'Especialidad no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': actualizada,
            'message': 'Especialidad actualizada exitosamente'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# -----------------------------------
# DELETE /api/especialidades/<id>
# -----------------------------------
@especialidades_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_especialidad(id):
    """
    DELETE /api/especialidades/:id
    Eliminar una especialidad
    """
    try:
        eliminada = especialidad_service.delete(id)
        
        if eliminada is None:
            return jsonify({
                'success': False,
                'error': 'Especialidad no encontrada'
            }), 404
        
        if not eliminada:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar la especialidad'
            }), 500
        
        return jsonify({
            'success': True,
            'message': 'Especialidad eliminada exitosamente'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
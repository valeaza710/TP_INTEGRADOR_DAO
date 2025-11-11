from flask import Blueprint, request, jsonify
from backend.services.paciente_service import PacienteService

# Crear blueprint
pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/api/pacientes')

# Instanciar servicio
paciente_service = PacienteService()

# -----------------------------------
# GET /api/pacientes
# -----------------------------------
@pacientes_bp.route('/', methods=['GET'])
def listar_pacientes():
    """GET /api/pacientes - Listar todos los pacientes"""
    try:
        pacientes = paciente_service.get_all()
        return jsonify({
            'success': True,
            'data': pacientes,
            'count': len(pacientes)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# -----------------------------------
# GET /api/pacientes/<id>
# -----------------------------------
@pacientes_bp.route('/<int:id>', methods=['GET'])
def obtener_paciente(id):
    """GET /api/pacientes/:id - Obtener un paciente por ID"""
    try:
        paciente = paciente_service.get_by_id(id)
        if not paciente:
            return jsonify({'success': False, 'error': 'Paciente no encontrado'}), 404

        return jsonify({'success': True, 'data': paciente}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# -----------------------------------
# POST /api/pacientes
# -----------------------------------
@pacientes_bp.route('/', methods=['POST'])
def crear_paciente():
    """POST /api/pacientes - Crear nuevo paciente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No se enviaron datos'}), 400

        nuevo = paciente_service.create(data)
        return jsonify({
            'success': True,
            'data': nuevo,
            'message': 'Paciente creado exitosamente'
        }), 201

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# -----------------------------------
# PUT /api/pacientes/<id>
# -----------------------------------
@pacientes_bp.route('/<int:id>', methods=['PUT'])
def actualizar_paciente(id):
    """PUT /api/pacientes/:id - Actualizar paciente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No se enviaron datos'}), 400

        actualizado = paciente_service.update(id, data)
        if not actualizado:
            return jsonify({'success': False, 'error': 'Paciente no encontrado'}), 404

        return jsonify({
            'success': True,
            'data': actualizado,
            'message': 'Paciente actualizado exitosamente'
        }), 200

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# -----------------------------------
# DELETE /api/paciente/<id>
# -----------------------------------
@pacientes_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_paciente(id):
    """DELETE /api/pacientes/:id - Eliminar paciente"""
    try:
        eliminado = paciente_service.delete(id)
        if eliminado is None:
            return jsonify({'success': False, 'error': 'Paciente no encontrado'}), 404

        if not eliminado:
            return jsonify({'success': False, 'error': 'No se pudo eliminar el paciente'}), 500

        return jsonify({'success': True, 'message': 'Paciente eliminado exitosamente'}), 200

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# -----------------------------------
# GET /api/pacientes/<dni>
# -----------------------------------
@pacientes_bp.route('/buscar', methods=['GET'])
def buscar_pacientes_por_dni():
    """
    GET /api/pacientes/buscar?dni=123
    Buscar pacientes cuyo DNI contenga el texto indicado
    """
    try:
        dni = request.args.get('dni', None)
        if not dni:
            return jsonify({'success': False, 'error': 'Debe especificar un valor de búsqueda (dni)'}), 400

        resultados = paciente_service.search_by_dni(dni)
        return jsonify({
            'success': True,
            'data': resultados,
            'count': len(resultados)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

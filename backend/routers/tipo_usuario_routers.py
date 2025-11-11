from flask import Blueprint, request, jsonify
from backend.services.tipo_usuario_service import TipoUsuarioService

tipo_usuario_bp = Blueprint('tipo_usuario', __name__, url_prefix='/api/tipo-usuario')

tipo_usuario_service = TipoUsuarioService()

# -----------------------------------
# GET /api/tipo-usuario/
# -----------------------------------
@tipo_usuario_bp.route('/', methods=['GET'])
def listar_tipos_usuario():
    try:
        tipos = tipo_usuario_service.get_all()
        return jsonify({
            "success": True,
            "data": tipos,
            "count": len(tipos)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# GET /api/tipo-usuario/<id>
# -----------------------------------
@tipo_usuario_bp.route('/<int:id>', methods=['GET'])
def obtener_tipo_usuario(id):
    try:
        tipo = tipo_usuario_service.get_by_id(id)
        if not tipo:
            return jsonify({"success": False, "error": "Tipo de usuario no encontrado"}), 404

        return jsonify({"success": True, "data": tipo}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# POST /api/tipo-usuario/
# -----------------------------------
@tipo_usuario_bp.route('/', methods=['POST'])
def crear_tipo_usuario():
    try:
        data = request.get_json()
        print(data)

        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        nuevo = tipo_usuario_service.create(data)

        return jsonify({
            "success": True,
            "data": nuevo,
            "message": "Tipo de usuario creado exitosamente"
        }), 201

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# PUT /api/tipo-usuario/<id>
# -----------------------------------
@tipo_usuario_bp.route('/<int:id>', methods=['PUT'])
def actualizar_tipo_usuario(id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        actualizado = tipo_usuario_service.update(id, data)

        if not actualizado:
            return jsonify({"success": False, "error": "Tipo de usuario no encontrado"}), 404

        return jsonify({
            "success": True,
            "data": actualizado,
            "message": "Tipo de usuario actualizado exitosamente"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# DELETE /api/tipo-usuario/<id>
# -----------------------------------
@tipo_usuario_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_tipo_usuario(id):
    try:
        eliminado = tipo_usuario_service.delete(id)

        if eliminado is None:
            return jsonify({"success": False, "error": "Tipo de usuario no encontrado"}), 404

        if not eliminado:
            return jsonify({"success": False, "error": "No se pudo eliminar el tipo de usuario"}), 500

        return jsonify({
            "success": True,
            "message": "Tipo de usuario eliminado exitosamente"
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

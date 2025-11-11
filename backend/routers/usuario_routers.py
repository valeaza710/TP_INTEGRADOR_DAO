from flask import Blueprint, request, jsonify
from backend.services.usuario_service import UsuarioService

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

usuario_service = UsuarioService()

# -----------------------------------
# GET /api/usuarios
# -----------------------------------
@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = usuario_service.get_all()
        return jsonify({
            "success": True,
            "data": usuarios,
            "count": len(usuarios)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# GET /api/usuarios/<id>
# -----------------------------------
@usuarios_bp.route('/<int:id>', methods=['GET'])
def obtener_usuario(id):
    try:
        usuario = usuario_service.get_by_id(id)
        if not usuario:
            return jsonify({"success": False, "error": "Usuario no encontrado"}), 404

        return jsonify({"success": True, "data": usuario}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# POST /api/usuarios
# -----------------------------------
@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        nuevo = usuario_service.create(data)
        return jsonify({
            "success": True,
            "data": nuevo,
            "message": "Usuario creado exitosamente"
        }), 201

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# PUT /api/usuarios/<id>
# -----------------------------------
@usuarios_bp.route('/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No se enviaron datos"}), 400

        actualizado = usuario_service.update(id, data)
        if not actualizado:
            return jsonify({"success": False, "error": "Usuario no encontrado"}), 404

        return jsonify({
            "success": True,
            "data": actualizado,
            "message": "Usuario actualizado exitosamente"
        }), 200

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -----------------------------------
# DELETE /api/usuarios/<id>
# -----------------------------------
@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        eliminado = usuario_service.delete(id)

        if eliminado is None:
            return jsonify({"success": False, "error": "Usuario no encontrado"}), 404

        if not eliminado:
            return jsonify({"success": False, "error": "No se pudo eliminar el usuario"}), 500

        return jsonify({"success": True, "message": "Usuario eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
        
# -----------------------------------
# POST /api/usuarios/login
# -----------------------------------
@usuarios_bp.route('/login', methods=['POST'])
def login_usuario():
    try:
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"success": False, "error": "Faltan credenciales"}), 400

        usuario = usuario_service.login(username, password)

        if not usuario:
            return jsonify({"success": False, "error": "Credenciales inválidas"}), 401

        # Armamos respuesta con datos del usuario
        return jsonify({
            "success": True,
            "user": {
                "id": usuario.id,
                "username": usuario.nombre_usuario,
                "rol": usuario.tipo_usuario.tipo if usuario.tipo_usuario else None
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

from flask import Blueprint, request, jsonify
from backend.services.usuario_service import UsuarioService

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')
usuario_service = UsuarioService()

@usuarios_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint de login
    POST /api/usuarios/login
    Body: { "username": "...", "password": "..." }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                "success": False,
                "message": "Faltan credenciales"
            }), 400
        
        # Llamar al servicio para autenticar
        usuario = usuario_service.login(data['username'], data['password'])
        
        if not usuario:
            return jsonify({
                "success": False,
                "message": "Credenciales incorrectas"
            }), 401
        
        # Obtener datos completos (usuario + paciente si existe)
        usuario_completo = usuario_service.get_usuario_completo(usuario.id)
        
        if usuario_completo and usuario_completo.get('paciente'):
            # Si tiene datos de paciente, retornarlos
            paciente = usuario_completo['paciente']
            return jsonify({
                "success": True,
                "user": {
                    "id": usuario.id,
                    "username": usuario.nombre_usuario,
                    "rol": usuario.tipo_usuario.tipo if usuario.tipo_usuario else "PACIENTE",
                    "nombre": paciente['nombre'],
                    "apellido": paciente['apellido'],
                    "email": paciente['email'],
                    "dni": paciente['dni']
                }
            }), 200
        else:
            # Si NO tiene paciente (ej: es admin o médico)
            return jsonify({
                "success": True,
                "user": {
                    "id": usuario.id,
                    "username": usuario.nombre_usuario,
                    "rol": usuario.tipo_usuario.tipo if usuario.tipo_usuario else "USUARIO"
                }
            }), 200
        
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return jsonify({
            "success": False,
            "message": "Error interno del servidor"
        }), 500


@usuarios_bp.route('/registro', methods=['POST'])
def registro():
    """
    Endpoint de registro
    POST /api/usuarios/registro
    Body: {
        "username": "...",
        "password": "...",
        "email": "...",
        "nombre": "...",
        "apellido": "...",
        "dni": "...",
        "edad": int (opcional),
        "fecha_nacimiento": "YYYY-MM-DD" (opcional)
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['username', 'password', 'email', 'nombre', 'apellido', 'dni']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "success": False,
                    "message": f"Falta el campo: {field}"
                }), 400
        
        # Crear usuario (el servicio crea tanto Usuario como Paciente)
        nuevo_usuario = usuario_service.crear_usuario(data)
        
        if not nuevo_usuario:
            return jsonify({
                "success": False,
                "message": "No se pudo crear el usuario. Verifique que el username, email o DNI no estén en uso."
            }), 400
        
        return jsonify({
            "success": True,
            "message": "Usuario registrado exitosamente",
            "user": {
                "id": nuevo_usuario.id,
                "username": nuevo_usuario.nombre_usuario
            }
        }), 201
        
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return jsonify({
            "success": False,
            "message": "Error al registrar usuario"
        }), 500


@usuarios_bp.route('/', methods=['GET'])
def get_all_usuarios():
    """
    Obtener todos los usuarios
    GET /api/usuarios/
    """
    try:
        usuarios = usuario_service.get_all()
        return jsonify({
            "success": True,
            "data": usuarios
        }), 200
    except Exception as e:
        print(f"❌ Error al obtener usuarios: {e}")
        return jsonify({
            "success": False,
            "message": "Error al obtener usuarios"
        }), 500


@usuarios_bp.route('/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    """
    Obtener un usuario por ID
    GET /api/usuarios/1
    """
    try:
        usuario = usuario_service.get_by_id(usuario_id)
        if not usuario:
            return jsonify({
                "success": False,
                "message": "Usuario no encontrado"
            }), 404
        
        return jsonify({
            "success": True,
            "data": usuario
        }), 200
    except Exception as e:
        print(f"❌ Error al obtener usuario: {e}")
        return jsonify({
            "success": False,
            "message": "Error al obtener usuario"
        }), 500
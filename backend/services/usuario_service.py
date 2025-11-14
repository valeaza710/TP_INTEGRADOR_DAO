from backend.repository.usuario_repository import UsuarioRepository
from backend.repository.paciente_repository import PacienteRepository
from backend.clases.usuario import Usuario
from backend.clases.paciente import Paciente
from backend.clases.tipo_usuario import TipoUsuario

class UsuarioService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.paciente_repo = PacienteRepository()

    # -------------------------------
    # LOGIN
    # -------------------------------
    def login(self, username, password):
        """Login básico sin hash"""
        try:
            usuario = self.usuario_repo.get_by_username(username)
            
            if not usuario:
                print(f"⚠️ Usuario '{username}' no encontrado")
                return None
            
            if usuario.contrasena == password:
                print(f"✅ Login exitoso para: {username}")
                return usuario
            
            print(f"⚠️ Contraseña incorrecta para: {username}")
            return None
            
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return None

    # -------------------------------
    # REGISTRO COMPLETO (Usuario + Paciente)
    # -------------------------------
# backend/services/usuario_service.py
    def crear_usuario(self, data: dict):
        """Crear usuario Y paciente en una transacción"""
        try:
            required_fields = ['username', 'password', 'email', 'nombre', 'apellido', 'dni']
            for field in required_fields:
                if not data.get(field):
                    print(f"⚠️ Falta el campo: {field}")
                    return None
            
            if self.usuario_repo.get_by_username(data['username']):
                print(f"⚠️ El username '{data['username']}' ya existe")
                return None
            
            if self.paciente_repo.get_by_email(data['email']):
                print(f"⚠️ El email '{data['email']}' ya está registrado")
                return None
            
            if self.paciente_repo.get_by_dni(data['dni']):
                print(f"⚠️ El DNI '{data['dni']}' ya está registrado")
                return None
            
            tipo_usuario = TipoUsuario(id=1, tipo="PACIENTE")
            nuevo_usuario = Usuario(
                nombre_usuario=data['username'],
                contrasena=data['password'],
                tipo_usuario=tipo_usuario
            )
            usuario_guardado = self.usuario_repo.save(nuevo_usuario)
            
            if not usuario_guardado:
                print("❌ No se pudo crear el usuario")
                return None
            
            nuevo_paciente = Paciente(
                nombre=data['nombre'],
                apellido=data['apellido'],
                dni=data['dni'],
                edad=data.get('edad'),
                fecha_nacimiento=data.get('fecha_nacimiento'),
                mail=data['email'],
                telefono=data.get('telefono'),
                direccion=data.get('direccion'),
                id_usuario=usuario_guardado.id
            )
            
            paciente_guardado = self.paciente_repo.save(nuevo_paciente)
            
            if not paciente_guardado:
                print("❌ No se pudo crear el paciente")
                self.usuario_repo.delete(usuario_guardado)
                return None
            
            print(f"✅ Registro completo: Usuario ID {usuario_guardado.id}, Paciente ID {paciente_guardado.id}")
            return usuario_guardado

        except Exception as e:
            print(f"❌ Error al crear usuario: {e}")
            return None

    # -------------------------------
    # OBTENER USUARIO COMPLETO (con datos de paciente)
    # -------------------------------
    def get_usuario_completo(self, usuario_id: int):
        """Obtener usuario con sus datos de paciente"""
        try:
            usuario = self.usuario_repo.get_by_id(usuario_id)
            if not usuario:
                return None
            
            paciente = self.paciente_repo.get_by_id_usuario(usuario_id)
            
            return {
                "id": usuario.id,
                "username": usuario.nombre_usuario,
                "rol": usuario.tipo_usuario.tipo if usuario.tipo_usuario else "PACIENTE",
                "paciente": {
                    "id": paciente.id,
                    "nombre": paciente.nombre,
                    "apellido": paciente.apellido,
                    "dni": paciente.dni,
                    "mail": paciente.mail,
                    "edad": paciente.edad,
                    "fecha_nacimiento": paciente.fecha_nacimiento,
                    "telefono": paciente.telefono,
                    "direccion": paciente.direccion
                } if paciente else None
            }
            
        except Exception as e:
            print(f"❌ Error en get_usuario_completo: {e}")
            return None

    # -------------------------------
    # LECTURAS
    # -------------------------------
    def get_all(self):
        """Obtener todos los usuarios"""
        try:
            usuarios = self.repository.get_all()
            return [self._to_dict(u) for u in usuarios]
        except Exception as e:
            print(f"❌ Error en get_all: {e}")
            raise Exception("Error al obtener usuarios")

    def get_by_id(self, usuario_id: int):
        """Obtener un usuario por ID"""
        try:
            usuario = self.repository.get_by_id(usuario_id)
            return self._to_dict(usuario) if usuario else None
        except Exception as e:
            print(f"❌ Error en get_by_id: {e}")
            raise Exception("Error al obtener usuario")

    # -------------------------------
    # CREAR (método legacy)
    # -------------------------------
    def create(self, data: dict):
        """Crear usuario (método antiguo, usar crear_usuario en su lugar)"""
        try:
            required = ["nombre_usuario", "contrasena"]
            for field in required:
                if not data.get(field) or str(data[field]).strip() == "":
                    raise ValueError(f"El campo '{field}' es obligatorio")

            tipo_usuario = None
            if "rol" in data and data["rol"]:
                tipo_usuario = TipoUsuario(id=data["rol"]["id"])

            usuario = Usuario(
                nombre_usuario=data["nombre_usuario"],
                contrasena=data["contrasena"],
                tipo_usuario=tipo_usuario
            )

            guardado = self.repository.save(usuario)
            if not guardado:
                raise Exception("No se pudo guardar el usuario")

            return self._to_dict(guardado)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"❌ Error en create: {e}")
            raise Exception("Error al crear usuario")

    # -------------------------------
    # UPDATE
    # -------------------------------
    def update(self, usuario_id: int, data: dict):
        """Modificar usuario"""
        try:
            usuario = self.repository.get_by_id(usuario_id)
            if not usuario:
                return None

            # Actualizar campos
            if "nombre_usuario" in data and data["nombre_usuario"].strip():
                usuario.nombre_usuario = data["nombre_usuario"]

            if "contrasena" in data and data["contrasena"].strip():
                usuario.contrasena = data["contrasena"]

            if "mail" in data:
                usuario.mail = data["mail"]
            
            if "nombre" in data:
                usuario.nombre = data["nombre"]
            
            if "apellido" in data:
                usuario.apellido = data["apellido"]
            
            if "dni" in data:
                usuario.dni = data["dni"]
            
            if "edad" in data:
                usuario.edad = data["edad"]
            
            if "fecha_nacimiento" in data:
                usuario.fecha_nacimiento = data["fecha_nacimiento"]

            if "rol" in data:
                usuario.tipo_usuario = (
                    TipoUsuario(id=data["rol"]) if data["rol"] else None
                )

            actualizado = self.repository.modify(usuario)
            if not actualizado:
                raise Exception("No se pudo actualizar el usuario")

            return self._to_dict(actualizado)

        except Exception as e:
            print(f"❌ Error en update: {e}")
            raise Exception("Error al modificar usuario")

    # -------------------------------
    # DELETE
    # -------------------------------
    def delete(self, usuario_id: int):
        """Eliminar usuario"""
        try:
            usuario = self.repository.get_by_id(usuario_id)
            if not usuario:
                return None

            eliminado = self.repository.delete(usuario)
            return eliminado

        except Exception as e:
            print(f"❌ Error en delete: {e}")
            raise Exception("Error al eliminar usuario")

    # -------------------------------
    # SERIALIZADOR
    # -------------------------------
    def _to_dict(self, u: Usuario):
        """Convertir Usuario a dict"""
        if not u:
            return None

        return {
            "id": u.id,
            "nombre_usuario": u.nombre_usuario,
            "mail": u.mail,
            "nombre": u.nombre,
            "apellido": u.apellido,
            "dni": u.dni,
            "edad": u.edad,
            "fecha_nacimiento": u.fecha_nacimiento,
            "tipo_usuario": {
                "id": u.tipo_usuario.id,
                "tipo": u.tipo_usuario.tipo
            } if u.tipo_usuario else None
        }
    
    def _to_dict_paciente(self, p: Paciente):
        """Convertir Paciente a dict"""
        if not p:
            return None

        return {
            "id": p.id,
            "nombre": p.nombre,
            "apellido": p.apellido,
            "dni": p.dni,
            "edad": p.edad,
            "fecha_nacimiento": p.fecha_nacimiento,
            "mail": p.mail,
            "telefono": p.telefono,
            "direccion": p.direccion,
            "id_usuario": p.id_usuario
        }
    

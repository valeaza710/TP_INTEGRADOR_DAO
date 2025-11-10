from backend.repository.usuario_repository import UsuarioRepository
from backend.clases.usuario import Usuario
from backend.clases.tipo_usuario import TipoUsuario

class UsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    # -------------------------------
    # LECTURAS
    # -------------------------------
    def get_all(self):
        """Obtener todos los usuarios"""
        try:
            usuarios = self.repository.get_all()
            return [self._to_dict(u) for u in usuarios]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener usuarios")

    def get_by_id(self, usuario_id: int):
        """Obtener un usuario por ID"""
        try:
            usuario = self.repository.get_by_id(usuario_id)
            return self._to_dict(usuario) if usuario else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener usuario")

    # -------------------------------
    # CREAR
    # -------------------------------
    def create(self, data: dict):
        """Crear un nuevo usuario"""
        try:
            # Validaciones básicas
            required = ["nombre_usuario", "contrasena"]
            for field in required:
                if not data.get(field) or str(data[field]).strip() == "":
                    raise ValueError(f"El campo '{field}' es obligatorio")

            # Tipo usuario
            tipo_usuario = None
            if "rol" in data and data["rol"]:
                tipo_usuario = TipoUsuario(id=data["rol"])

            # Crear objeto
            usuario = Usuario(
                nombre_usuario=data["nombre_usuario"],
                contrasena=data["contrasena"],
                tipo_usuario=tipo_usuario
            )

            # Guardar
            guardado = self.repository.save(usuario)
            if not guardado:
                raise Exception("No se pudo guardar el usuario")

            return self._to_dict(guardado)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
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

            # Actualizamos campos
            if "nombre_usuario" in data and data["nombre_usuario"].strip():
                usuario.nombre_usuario = data["nombre_usuario"]

            if "contrasena" in data and data["contrasena"].strip():
                usuario.contrasena = data["contrasena"]

            if "rol" in data:
                usuario.tipo_usuario = (
                    TipoUsuario(id=data["rol"]) if data["rol"] else None
                )

            actualizado = self.repository.modify(usuario)
            if not actualizado:
                raise Exception("No se pudo actualizar el usuario")

            return self._to_dict(actualizado)

        except Exception as e:
            print(f"Error en update: {e}")
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
            print(f"Error en delete: {e}")
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
            "contrasena": u.contrasena,  # Podés ocultarla si querés
            "tipo_usuario": {
                "id": u.tipo_usuario.id,
                "tipo": u.tipo_usuario.tipo
            } if u.tipo_usuario else None
        }

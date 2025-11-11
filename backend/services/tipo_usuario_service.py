from backend.repository.tipo_usuario_repository import TipoUsuarioRepository
from backend.clases.tipo_usuario import TipoUsuario

class TipoUsuarioService:
    def __init__(self):
        self.repository = TipoUsuarioRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            tipos = self.repository.get_all()
            return [self._to_dict(t) for t in tipos]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener tipos de usuario")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, tipo_id: int):
        try:
            tipo = self.repository.get_by_id(tipo_id)
            return self._to_dict(tipo) if tipo else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener tipo de usuario")

    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            if not data.get("tipo") or data["tipo"].strip() == "":
                raise ValueError("El campo 'tipo' es obligatorio")

            nuevo_tipo = TipoUsuario(
                tipo=data["tipo"]
            )

            guardado = self.repository.save(nuevo_tipo)
            if not guardado:
                raise Exception("No se pudo guardar el tipo de usuario")

            return self._to_dict(guardado)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear tipo de usuario")

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, tipo_id: int, data: dict):
        try:
            tipo = self.repository.get_by_id(tipo_id)
            if not tipo:
                return None

            if "tipo" in data and data["tipo"].strip():
                tipo.tipo = data["tipo"]

            actualizado = self.repository.modify(tipo)

            if not actualizado:
                raise Exception("No se pudo actualizar el tipo de usuario")

            return self._to_dict(actualizado)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar tipo de usuario")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, tipo_id: int):
        try:
            tipo = self.repository.get_by_id(tipo_id)
            if not tipo:
                return None

            eliminado = self.repository.delete(tipo)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar tipo de usuario")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, t: TipoUsuario):
        if not t:
            return None

        return {
            "id": t.id,
            "tipo": t.tipo
        }

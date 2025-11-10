from repository.estado_turno_repository import EstadoTurnoRepository
from clases.estado_turno import EstadoTurno


class EstadoTurnoService:
    def __init__(self):
        self.repository = EstadoTurnoRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            estados = self.repository.get_all()
            return [self._to_dict(e) for e in estados]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener estados de turno")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, estado_id: int):
        try:
            estado = self.repository.get_by_id(estado_id)
            return self._to_dict(estado) if estado else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener estado de turno")

    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            if not data.get("nombre"):
                raise ValueError("El campo 'nombre' es obligatorio")

            nuevo_estado = EstadoTurno(nombre=data["nombre"])

            guardado = self.repository.save(nuevo_estado)
            if not guardado:
                raise Exception("No se pudo guardar el estado de turno")

            completo = self.repository.get_by_id(guardado.id)
            return self._to_dict(completo)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear estado de turno")

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, estado_id: int, data: dict):
        try:
            estado = self.repository.get_by_id(estado_id)
            if not estado:
                return None

            if "nombre" in data and data["nombre"]:
                estado.nombre = data["nombre"]

            actualizado = self.repository.modify(estado)
            if not actualizado:
                raise Exception("No se pudo actualizar el estado de turno")

            completo = self.repository.get_by_id(estado_id)
            return self._to_dict(completo)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar estado de turno")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, estado_id: int):
        try:
            estado = self.repository.get_by_id(estado_id)
            if not estado:
                return None

            eliminado = self.repository.delete(estado)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar estado de turno")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, e: EstadoTurno):
        if not e:
            return None

        return {
            "id": e.id,
            "nombre": e.nombre
        }

from repository.especialidad_repository import EspecialidadRepository
from clases.especialidad import Especialidad


class EspecialidadService:
    def __init__(self):
        self.repository = EspecialidadRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            especialidades = self.repository.get_all()
            return [self._to_dict(e) for e in especialidades]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener especialidades")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, especialidad_id: int):
        try:
            especialidad = self.repository.get_by_id(especialidad_id)
            return self._to_dict(especialidad) if especialidad else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener especialidad")

    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            # Validar campo obligatorio
            if not data.get("nombre") or data["nombre"].strip() == "":
                raise ValueError("El campo 'nombre' es obligatorio")

            # Verificar si ya existe una especialidad con el mismo nombre
            if self.repository.exists_by_nombre(data["nombre"]):
                raise ValueError("Ya existe una especialidad con ese nombre")

            # Crear objeto Especialidad
            nueva_especialidad = Especialidad(nombre=data["nombre"])

            # Guardar en BD
            guardada = self.repository.save(nueva_especialidad)
            if not guardada:
                raise Exception("No se pudo guardar la especialidad")

            # Devolver el objeto completo guardado
            completa = self.repository.get_by_id(guardada.id)
            return self._to_dict(completa)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear especialidad")

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, especialidad_id: int, data: dict):
        try:
            especialidad = self.repository.get_by_id(especialidad_id)
            if not especialidad:
                return None

            # Actualizar solo si el nombre fue enviado
            if "nombre" in data and data["nombre"].strip() != "":
                especialidad.nombre = data["nombre"]

            actualizada = self.repository.modify(especialidad)
            if not actualizada:
                raise Exception("No se pudo actualizar la especialidad")

            completa = self.repository.get_by_id(especialidad_id)
            return self._to_dict(completa)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar especialidad")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, especialidad_id: int):
        try:
            especialidad = self.repository.get_by_id(especialidad_id)
            if not especialidad:
                return None

            # Validar que no tenga médicos asociados antes de eliminar
            if self.repository.tiene_medicos_asociados(especialidad_id):
                raise ValueError("No se puede eliminar una especialidad con médicos asociados")

            eliminado = self.repository.delete(especialidad)
            return eliminado

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar especialidad")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, e: Especialidad):
        if not e:
            return None

        return {
            "id": e.id,
            "nombre": e.nombre
        }

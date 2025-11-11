from backend.repository.enfermedades_repository import EnfermedadRepository
from backend.clases.enfermedad import Enfermedad


class EnfermedadService:
    def __init__(self):
        self.repository = EnfermedadRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            enfermedades = self.repository.get_all()
            return [self._to_dict(e) for e in enfermedades]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener enfermedades")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, enfermedad_id: int):
        try:
            enfermedad = self.repository.get_by_id(enfermedad_id)
            return self._to_dict(enfermedad) if enfermedad else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener enfermedad")

    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            # Validar campo obligatorio
            if not data.get("nombre") or str(data["nombre"]).strip() == "":
                raise ValueError("El campo 'nombre' es obligatorio")

            # Crear objeto Enfermedad
            nueva_enfermedad = Enfermedad(
                nombre=data["nombre"],
                descripcion=data.get("descripcion")
            )

            # Guardar en BD
            guardada = self.repository.save(nueva_enfermedad)
            if not guardada:
                raise Exception("No se pudo guardar la enfermedad")

            # Retornar enfermedad guardada
            completa = self.repository.get_by_id(guardada.id)
            return self._to_dict(completa)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear enfermedad")

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, enfermedad_id: int, data: dict):
        try:
            enfermedad = self.repository.get_by_id(enfermedad_id)
            if not enfermedad:
                return None

            # Actualizar campos enviados
            if "nombre" in data and data["nombre"] is not None:
                enfermedad.nombre = data["nombre"]
            if "descripcion" in data:
                enfermedad.descripcion = data["descripcion"]

            actualizada = self.repository.modify(enfermedad)
            if not actualizada:
                raise Exception("No se pudo actualizar la enfermedad")

            completa = self.repository.get_by_id(enfermedad_id)
            return self._to_dict(completa)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar enfermedad")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, enfermedad_id: int):
        try:
            enfermedad = self.repository.get_by_id(enfermedad_id)
            if not enfermedad:
                return None

            eliminado = self.repository.delete(enfermedad)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar enfermedad")

    # ------------------------------------
    # SEARCH BY NOMBRE
    # ------------------------------------
    def search_by_nombre(self, nombre_parcial: str):
        try:
            enfermedades = self.repository.search_by_nombre(nombre_parcial)
            return [self._to_dict(e) for e in enfermedades]
        except Exception as e:
            print(f"Error en search_by_nombre: {e}")
            raise Exception("Error al buscar enfermedades por nombre")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, e: Enfermedad):
        if not e:
            return None

        return {
            "id": e.id,
            "nombre": e.nombre,
            "descripcion": e.descripcion
        }

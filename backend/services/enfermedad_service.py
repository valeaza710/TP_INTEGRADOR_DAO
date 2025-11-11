from backend.repository.enfermedades_repository import EnfermedadRepository
from backend.clases.enfermedad import Enfermedad

class EnfermedadService:
    def __init__(self):
        self.repository = EnfermedadRepository()

    def get_all(self):
        """Obtener todas las enfermedades"""
        try:
            enfermedades = self.repository.get_all()
            return [self._to_dict(e) for e in enfermedades]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener enfermedades")

    def get_by_id(self, enfermedad_id):
        """Obtener enfermedad por ID"""
        try:
            enfermedad = self.repository.get_by_id(enfermedad_id)
            return self._to_dict(enfermedad) if enfermedad else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener la enfermedad")

    def create(self, data):
        """Crear nueva enfermedad"""
        try:
            if not data.get('nombre') or str(data['nombre']).strip() == '':
                raise ValueError("El campo 'nombre' es obligatorio")

            nueva_enfermedad = Enfermedad(
                nombre=data['nombre'],
                descripcion=data.get('descripcion')
            )

            enfermedad_guardada = self.repository.save(nueva_enfermedad)
            if not enfermedad_guardada:
                raise Exception("No se pudo guardar la enfermedad")

            return self._to_dict(enfermedad_guardada)
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear la enfermedad")

    def update(self, enfermedad_id, data):
        """Actualizar una enfermedad"""
        try:
            enfermedad = self.repository.get_by_id(enfermedad_id)
            if not enfermedad:
                return None

            if 'nombre' in data and data['nombre'] is not None:
                enfermedad.nombre = data['nombre']
            if 'descripcion' in data:
                enfermedad.descripcion = data['descripcion']

            actualizada = self.repository.modify(enfermedad)
            if not actualizada:
                raise Exception("No se pudo actualizar la enfermedad")

            return self._to_dict(actualizada)
        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar la enfermedad")

    def delete(self, enfermedad_id):
        """Eliminar enfermedad"""
        try:
            enfermedad = self.repository.get_by_id(enfermedad_id)
            if not enfermedad:
                return None
            eliminado = self.repository.delete(enfermedad)
            return eliminado
        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar la enfermedad")

    def search_by_nombre(self, nombre_parcial: str):
        """Buscar enfermedades por coincidencia parcial de nombre"""
        try:
            enfermedades = self.repository.search_by_nombre(nombre_parcial)
            return [self._to_dict(e) for e in enfermedades]
        except Exception as e:
            print(f"Error en search_by_nombre: {e}")
            raise Exception("Error al buscar enfermedades por nombre")

    def _to_dict(self, enfermedad: Enfermedad):
        if not enfermedad:
            return None
        return {
            'id': enfermedad.id,
            'nombre': enfermedad.nombre,
            'descripcion': enfermedad.descripcion
        }

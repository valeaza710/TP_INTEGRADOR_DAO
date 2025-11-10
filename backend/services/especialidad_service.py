from backend.repository.especialidad_repository import EspecialidadRepository
from backend.clases.especialidad import Especialidad

class EspecialidadService:
    def __init__(self):
        self.repository = EspecialidadRepository()
    
    def get_all(self):
        """Obtener todas las especialidades"""
        try:
            especialidades = self.repository.get_all()
            return [self._to_dict(e) for e in especialidades]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener especialidades")
    

    def get_by_id(self, especialidad_id):
        """Obtener una especialidad por ID"""
        try:
            especialidad = self.repository.get_by_id(especialidad_id)
            return self._to_dict(especialidad) if especialidad else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener la especialidad")
        
    
    def create(self, data):
        """Crear nueva especialidad"""
        try:
            # Validación simple
            if not data.get('nombre') or data['nombre'].strip() == '':
                raise ValueError('El nombre es obligatorio')
            
            # Verificar que no exista (usando método sugerido más abajo)
            if self.repository.exists_by_nombre(data['nombre']):
                 raise ValueError('Ya existe una especialidad con ese nombre')
            
            # Crear objeto Especialidad
            nueva_especialidad = Especialidad(
                nombre=data['nombre']
            )
            
            # Guardar en BD
            especialidad_guardada = self.repository.save(nueva_especialidad)
            
            if not especialidad_guardada:
                raise Exception("No se pudo guardar la especialidad")
            
            return self._to_dict(especialidad_guardada)
        
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear la especialidad")
    
    def update(self, especialidad_id, data):
        """Actualizar especialidad"""
        try:
            # Buscar especialidad existente
            especialidad = self.repository.get_by_id(especialidad_id)
            if not especialidad:
                return None
            
            # Actualizar campos
            if 'nombre' in data and data['nombre'].strip() != '':
                especialidad.nombre = data['nombre']
            
            # Guardar cambios
            especialidad_actualizada = self.repository.modify(especialidad)
            
            if not especialidad_actualizada:
                raise Exception("No se pudo actualizar la especialidad")
            
            return self._to_dict(especialidad_actualizada)
        
        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar la especialidad")
    
    def delete(self, especialidad_id):
        """Eliminar especialidad"""
        try:
            # Buscar especialidad
            especialidad = self.repository.get_by_id(especialidad_id)
            if not especialidad:
                return None
            
            # Verificar que no esté asociada a médicos (método sugerido más abajo)
            if self.repository.tiene_medicos_asociados(especialidad_id):
                 raise ValueError("No se puede eliminar una especialidad con médicos asociados")
            
            # Eliminar
            eliminada = self.repository.delete(especialidad)
            return eliminada
        
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar la especialidad")
    
    def _to_dict(self, especialidad):
        """Convertir objeto Especialidad a diccionario"""
        if not especialidad:
            return None
        return {
            'id': especialidad.id,
            'nombre': especialidad.nombre
        }
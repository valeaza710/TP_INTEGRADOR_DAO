from backend.repository.medico_repository import MedicoRepository
from backend.clases.medico import Medico

class MedicoService:
    def __init__(self):
        self.repository = MedicoRepository()

    def get_all(self):
        """Obtener todos los médicos"""
        try:
            medicos = self.repository.get_all()
            return [self._to_dict(m) for m in medicos]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener médicos")
    
    def get_by_id(self, medico_id):
        """Obtener un médico por ID"""
        try:
            medico = self.repository.get_by_id(medico_id)
            return self._to_dict(medico) if medico else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener el médico")
    
    def create(self, data):
        """Crear nuevo médico"""
        try:
            # Validación simple
            if not data.get('nombre') or data['nombre'].strip() == '':
                raise ValueError('El nombre es obligatorio')
            if not data.get('apellido') or data['apellido'].strip() == '':
                raise ValueError('El apellido es obligatorio')
            
            # Crear objeto Medico
            nuevo_medico = Medico(
                nombre=data['nombre'],
                apellido=data['apellido'],
                dni=data.get('dni'),
                matricula=data.get('matricula'),
                telefono=data.get('telefono'),
                mail=data.get('mail'),
                direccion=data.get('direccion'),
                usuario=None  # Asignar usuario si es necesario
            )
            
            # Guardar en BD
            medico_guardado = self.repository.save(nuevo_medico)
            
            if not medico_guardado:
                raise Exception("No se pudo guardar el médico")
            
            return self._to_dict(medico_guardado)
        
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear el médico")

def _to_dict(self, medico: Medico):       
        if not medico:
            return None
        return {
            'id': medico.id,
            'nombre': medico.nombre,
            'apellido': medico.apellido,
            'dni': medico.dni,
            'matricula': medico.matricula,
            'telefono': medico.telefono,
            'mail': medico.mail,
            'direccion': medico.direccion,
            'usuario': medico.usuario  # Ajustar según cómo se maneje el usuario
        }


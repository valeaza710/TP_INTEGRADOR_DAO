from repository.paciente_repository import PacienteRepository
from clases.paciente import Paciente
from clases.usuario import Usuario

class PacienteService:
    def __init__(self):
        self.repository = PacienteRepository()

    def get_all(self):
        """Obtener todos los pacientes"""
        try:
            pacientes = self.repository.get_all()
            return [self._to_dict(p) for p in pacientes]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener pacientes")

    def get_by_id(self, paciente_id):
        """Obtener un paciente por ID"""
        try:
            paciente = self.repository.get_by_id(paciente_id)
            return self._to_dict(paciente) if paciente else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener el paciente")

    def create(self, data):
        """Crear un nuevo paciente"""
        try:
            # Validaciones mínimas
            campos_obligatorios = ['nombre', 'apellido', 'dni', 'edad', 'fecha_nacimiento', 'mail']
            for campo in campos_obligatorios:
                if not data.get(campo) or str(data[campo]).strip() == '':
                    raise ValueError(f"El campo '{campo}' es obligatorio")

            # Crear objeto Usuario si hay id_usuario
            usuario = data.get('id_usuario', None)
            usuario_obj = Usuario(id=usuario) if usuario else None

            nuevo_paciente = Paciente(
                nombre=data['nombre'],
                apellido=data['apellido'],
                dni=data['dni'],
                edad=data['edad'],
                fecha_nacimiento=data['fecha_nacimiento'],
                mail=data['mail'],
                telefono=data.get('telefono'),
                direccion=data.get('direccion'),
                usuario=usuario_obj
            )

            paciente_guardado = self.repository.save(nuevo_paciente)
            if not paciente_guardado:
                raise Exception("No se pudo guardar el paciente")

            return self._to_dict(paciente_guardado)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear el paciente")

    def update(self, paciente_id, data):
        """Actualizar un paciente"""
        try:
            paciente = self.repository.get_by_id(paciente_id)
            if not paciente:
                return None

            # Actualizar los campos enviados
            for campo in ['nombre', 'apellido', 'dni', 'edad', 'fecha_nacimiento', 'mail', 'telefono', 'direccion']:
                if campo in data and data[campo] is not None:
                    setattr(paciente, campo, data[campo])

            # Actualizar usuario asociado si se envía
            if 'id_usuario' in data:
                paciente.usuario = Usuario(id=data['id_usuario']) if data['id_usuario'] else None

            paciente_actualizado = self.repository.modify(paciente)
            if not paciente_actualizado:
                raise Exception("No se pudo actualizar el paciente")

            return self._to_dict(paciente_actualizado)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar el paciente")

    def delete(self, paciente_id):
        """Eliminar un paciente"""
        try:
            paciente = self.repository.get_by_id(paciente_id)
            if not paciente:
                return None

            eliminado = self.repository.delete(paciente)
            return eliminado
        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar el paciente")

    def _to_dict(self, paciente):
        """Convertir objeto Paciente a diccionario"""
        if not paciente:
            return None

        return {
            'id': paciente.id,
            'nombre': paciente.nombre,
            'apellido': paciente.apellido,
            'dni': paciente.dni,
            'edad': paciente.edad,
            'fecha_nacimiento': str(paciente.fecha_nacimiento),
            'mail': paciente.mail,
            'telefono': paciente.telefono,
            'direccion': paciente.direccion,
            'usuario': {
                'id': paciente.usuario.id,
                'nombre_usuario': getattr(paciente.usuario, 'nombre_usuario', None),
                'rol': getattr(paciente.usuario, 'rol', None)
            } if paciente.usuario else None
        }
    
    def search_by_dni(self, dni_parcial: str):
        """Buscar pacientes cuyo DNI contenga el texto indicado"""
        try:
            pacientes = self.repository.search_by_dni(dni_parcial)
            return [self._to_dict(p) for p in pacientes]
        except Exception as e:
            print(f"Error en search_by_dni: {e}")
            raise Exception("Error al buscar pacientes por DNI")

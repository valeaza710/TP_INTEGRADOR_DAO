from backend.repository.paciente_repository import PacienteRepository
from backend.clases.paciente import Paciente
from backend.clases.usuario import Usuario


class PacienteService:
    def __init__(self):
        self.repository = PacienteRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            pacientes = self.repository.get_all()
            return [self._to_dict(p) for p in pacientes]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener pacientes")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, paciente_id: int):
        try:
            print(f"🔹 Buscando paciente con ID={paciente_id}")  # debug
            paciente = self.repository.get_by_id(paciente_id)
            print(f"🔹 Resultado raw de repository.get_by_id: {paciente}")  # debug

            if paciente:
                paciente_dict = self._to_dict(paciente)
                print(f"✅ Paciente convertido a dict: {paciente_dict}")  # debug
                return paciente_dict
            else:
                print("ℹ️ No se encontró paciente")
                return None
        except Exception as e:
            print(f"❌ Error en get_by_id: {e}")
            raise Exception("Error al obtener paciente")


    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            campos_obligatorios = ['nombre', 'apellido', 'dni', 'edad', 'fecha_nacimiento', 'mail']
            for campo in campos_obligatorios:
                if not data.get(campo) or str(data[campo]).strip() == '':
                    raise ValueError(f"El campo '{campo}' es obligatorio")

            usuario_obj = Usuario(id=data['id_usuario']) if data.get('id_usuario') else None

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

            guardado = self.repository.save(nuevo_paciente)
            if not guardado:
                raise Exception("No se pudo guardar el paciente")

            completo = self.repository.get_by_id(guardado.id)
            return self._to_dict(completo)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear paciente")

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, paciente_id: int, data: dict):
        try:
            paciente = self.repository.get_by_id(paciente_id)
            if not paciente:
                return None

            for campo in ['nombre', 'apellido', 'dni', 'edad', 'fecha_nacimiento', 'mail', 'telefono', 'direccion']:
                if campo in data and data[campo] is not None:
                    setattr(paciente, campo, data[campo])

            if 'id_usuario' in data:
                paciente.usuario = Usuario(id=data['id_usuario']) if data['id_usuario'] else None

            actualizado = self.repository.modify(paciente)
            if not actualizado:
                raise Exception("No se pudo actualizar el paciente")

            completo = self.repository.get_by_id(paciente_id)
            return self._to_dict(completo)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar paciente")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, paciente_id: int):
        try:
            paciente = self.repository.get_by_id(paciente_id)
            if not paciente:
                return None

            eliminado = self.repository.delete(paciente)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar paciente")

    # ------------------------------------
    # SEARCH BY DNI
    # ------------------------------------
    # Buscar por DNI parcial
    def search_by_dni(self, dni_parcial: str):
        pacientes = self.repository.get_by_dni(dni_parcial)
        print(pacientes)
        return [self._to_dict(p) for p in pacientes]

    # Serializador simple que evita errores de atributos
    def _to_dict(self, p: Paciente):
        return {
            'id': p.id,
            'nombre': p.nombre,
            'apellido': p.apellido,
            'dni': p.dni
            # omite campos complicados por ahora
        }


    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id_completo(self, paciente_id: int):
        try:
            paciente = self.repository.get_by_id(paciente_id)
            return self._to_dict_viejo(paciente) if paciente else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener paciente")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict_viejo(self, p: Paciente):
        if not p:
            return None

        return {
            'id': p.id,
            'nombre': p.nombre,
            'apellido': p.apellido,
            'dni': p.dni,
            'edad': p.edad,
            'fecha_nacimiento': str(p.fecha_nacimiento),
            'mail': p.mail,
            'telefono': p.telefono,
            'direccion': p.direccion,
            'usuario': {
                'id': p.usuario.id,
                'nombre_usuario': getattr(p.usuario, 'nombre_usuario', None),
                'tipo_usuario': getattr(p.usuario.tipo_usuario, 'tipo_usuario', None)
            } if p.usuario else None
        }


    def get_basic_info(self):
    #Devuelve solo nombre, apellido y dni de todos los pacientes
        try:
            pacientes = self.repository.get_all()
            return [
                {
                    'id': p.id,
                    'nombre': p.nombre,
                    'apellido': p.apellido,
                    'dni': p.dni
                }
                for p in pacientes
            ]
        except Exception as e:
            print(f"Error en get_basic_info_all: {e}")
            raise Exception("Error al obtener pacientes básicos")

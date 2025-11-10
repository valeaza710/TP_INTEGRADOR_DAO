from repository.medico_repository import MedicoRepository
from clases.medico import Medico
from clases.especialidad import Especialidad
from clases.usuario import Usuario

class MedicoService:
    def __init__(self):
        self.repository = MedicoRepository()

    # -------------------------------
    # LECTURAS
    # -------------------------------
    def get_all(self):
        """Obtener todos los médicos"""
        try:
            medicos = self.repository.get_all()
            return [self._to_dict(m) for m in medicos]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener médicos")

    def get_by_id(self, medico_id: int):
        """Obtener médico por ID"""
        try:
            medico = self.repository.get_by_id(medico_id)
            return self._to_dict(medico) if medico else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener médico")

    # -------------------------------
    # CREAR
    # -------------------------------
    def create(self, data: dict):
        """Crear un nuevo médico"""

        try:
            # Validaciones
            required = ["nombre", "apellido", "matricula"]
            for field in required:
                if not data.get(field) or data[field].strip() == "":
                    raise ValueError(f"El campo '{field}' es obligatorio")

            # Validación simple de especialidades
            especialidades = []
            if "especialidades" in data:
                for esp in data['especialidades']:
                    especialidades.append(Especialidad(id=esp))

            # Si viene usuario:
            usuario = None
            if "usuario" in data and data["usuario"]:
                usuario = Usuario(
                    id=data["usuario"]["id"],
                    nombre_usuario=None,
                    contrasena=None
                )

            # Crear objeto
            medico = Medico(
                nombre=data["nombre"],
                apellido=data["apellido"],
                dni=data.get("dni"),
                matricula=data["matricula"],
                telefono=data.get("telefono"),
                mail=data.get("mail"),
                direccion=data.get("direccion"),
                especialidades=especialidades,
                usuario=usuario
            )

            # Guardar
            medico_guardado = self.repository.save(medico)
            if not medico_guardado:
                raise Exception("No se pudo guardar el médico")
            
            return self._to_dict(medico_guardado)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear médico")

    # -------------------------------
    # UPDATE
    # -------------------------------
    def update(self, medico_id, data):
        """Modificar médico"""

        try:
            medico = self.repository.get_by_id(medico_id)
            if not medico:
                return None

            # Actualizamos campos
            for key in ["nombre", "apellido", "dni", "matricula", "telefono", "mail", "direccion"]:
                if key in data and data[key] is not None:
                    if isinstance(data[key], str) and data[key].strip() == "":
                        continue
                    setattr(medico, key, data[key])

            # Actualizar especialidades
            if "especialidades" in data:
                medico.especialidades = [Especialidad(id=eid) for eid in data["especialidades"]]

            # Actualizar usuario asociado
            if "usuario" in data:
                if data["usuario"] is None:
                    medico.usuario = None
                else:
                    medico.usuario = Usuario(id=data["usuario"]["id"])

            medico_actualizado = self.repository.modify(medico)
            if not medico_actualizado:
                raise Exception("No se pudo actualizar el médico")

            return self._to_dict(medico_actualizado)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al modificar médico")

    # -------------------------------
    # DELETE
    # -------------------------------
    def delete(self, medico_id):
        """Eliminar médico"""
        try:
            medico = self.repository.get_by_id(medico_id)
            if not medico:
                return None

            eliminado = self.repository.delete(medico)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar médico")

    # -------------------------------
    # SERIALIZADOR
    # -------------------------------
    def _to_dict(self, m: Medico):
        """Convertir objeto Médico a diccionario"""
        if not m:
            return None
        
        return {
            "id": m.id,
            "nombre": m.nombre,
            "apellido": m.apellido,
            "dni": m.dni,
            "matricula": m.matricula,
            "telefono": m.telefono,
            "mail": m.mail,
            "direccion": m.direccion,
            "especialidades": [
                {"id": esp.id, "nombre": esp.nombre}
                for esp in m.especialidades
            ],
            "usuario": {
                "id": m.usuario.id,
                "nombre_usuario": m.usuario.nombre_usuario
            } if m.usuario else None
        }

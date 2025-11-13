from backend.repository.medico_repository import MedicoRepository
from backend.clases.medico import Medico
from backend.clases.usuario import Usuario
from backend.clases.especialidad import Especialidad


class MedicoService:
    def __init__(self):
        self.repository = MedicoRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            medicos = self.repository.get_all()
            return [self._to_dict(m) for m in medicos]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener médicos")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, medico_id: int):
        try:
            medico = self.repository.get_by_id(medico_id)
            return self._to_dict(medico) if medico else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener médico")

    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            # Validaciones básicas
            if not data.get("nombre") or data["nombre"].strip() == "":
                raise ValueError("El campo 'nombre' es obligatorio")
            if not data.get("apellido") or data["apellido"].strip() == "":
                raise ValueError("El campo 'apellido' es obligatorio")

            usuario_obj = Usuario(id=data["id_usuario"]) if data.get("id_usuario") else None

            # ✅ Especialidades (puede venir una lista de objetos o IDs)
            especialidades = []
            if data.get("especialidades"):
                for e in data["especialidades"]:
                    if isinstance(e, dict):
                        especialidades.append(Especialidad(id=e.get("id"), nombre=e.get("nombre")))
                    else:
                        especialidades.append(Especialidad(id=e))

            nuevo_medico = Medico(
                nombre=data["nombre"],
                apellido=data["apellido"],
                dni=data.get("dni"),
                matricula=data.get("matricula"),
                telefono=data.get("telefono"),
                mail=data.get("mail"),
                direccion=data.get("direccion"),
                usuario=usuario_obj,
                especialidades=especialidades
            )

            guardado = self.repository.save(nuevo_medico)
            if not guardado:
                raise Exception("No se pudo guardar el médico")

            completo = self.repository.get_by_id(guardado.id)
            return self._to_dict(completo)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear médico")

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, medico_id: int, data: dict):
        try:
            medico = self.repository.get_by_id(medico_id)
            if not medico:
                return None

            for campo in ["nombre", "apellido", "dni", "matricula", "telefono", "mail", "direccion"]:
                if campo in data and data[campo] is not None:
                    setattr(medico, campo, data[campo])

            if "id_usuario" in data:
                medico.usuario = Usuario(id=data["id_usuario"]) if data["id_usuario"] else None

            actualizado = self.repository.modify(medico)
            if not actualizado:
                raise Exception("No se pudo actualizar el médico")

            completo = self.repository.get_by_id(medico_id)
            return self._to_dict(completo)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar médico")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, medico_id: int):
        try:
            medico = self.repository.get_by_id(medico_id)
            if not medico:
                return None

            eliminado = self.repository.delete(medico)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar médico")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, m: Medico):
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
            "especialidades": [e.nombre for e in m.especialidades] if m.especialidades else [],
            "usuario": {
                "id": m.usuario.id,
                "nombre_usuario": getattr(m.usuario, "nombre_usuario", None),
                "rol": getattr(m.usuario, "rol", None)
            } if m.usuario else None
        }


    def get_all_basic(self):
    #Devuelve una lista simple de médicos con sus datos principales
        try:
            medicos = self.repository.get_all()
            for m in medicos:
                print(f"{m.nombre} {m.apellido} -> {[e.nombre for e in m.especialidades]}")
            return [
                {
                    'id': m.id,
                    'nombre': m.nombre,
                    'apellido': m.apellido,
                    "especialidades": [{"id": e.id, "nombre": e.nombre} for e in getattr(m, "especialidades", [])]
                    
                }
                
                for m in medicos
            ]
            
        except Exception as e:
            print(f"Error en get_all_basic: {e}")
            raise Exception("Error al obtener médicos básicos")

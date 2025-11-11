from backend.repository.horario_medico_repository import HorarioMedicoRepository
from backend.clases.horario_medico import HorarioMedico
from backend.clases.medico import Medico


class HorarioMedicoService:
    def __init__(self):
        self.repository = HorarioMedicoRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            horarios = self.repository.get_all()
            return [self._to_dict(h) for h in horarios]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener horarios médicos")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, horario_id: int):
        try:
            horario = self.repository.get_by_id(horario_id)
            return self._to_dict(horario) if horario else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener horario médico")

    # ------------------------------------
    # GET BY MEDICO
    # ------------------------------------
    def get_by_medico(self, medico_id: int):
        try:
            horarios = self.repository.get_by_medico(Medico(id=medico_id))
            return [self._to_dict(h) for h in horarios]
        except Exception as e:
            print(f"Error en get_by_medico: {e}")
            raise Exception("Error al obtener horarios por médico")

    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            if not data.get("id_medico"):
                raise ValueError("El campo 'id_medico' es obligatorio")

            nuevo_horario = HorarioMedico(
                medico=Medico(id=data["id_medico"]),
                mes=data.get("mes"),
                anio=data.get("anio"),
                dia_semana=data.get("dia_semana"),
                hora_inicio=data.get("hora_inicio"),
                hora_fin=data.get("hora_fin"),
                duracion_turno_min=data.get("duracion_turno_min")
            )

            guardado = self.repository.save(nuevo_horario)
            if not guardado:
                raise Exception("No se pudo guardar el horario médico")

            completo = self.repository.get_by_id(guardado.id)
            return self._to_dict(completo)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear horario médico")

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, horario_id: int, data: dict):
        try:
            horario = self.repository.get_by_id(horario_id)
            if not horario:
                return None

            for campo in ["mes", "anio", "dia_semana", "hora_inicio", "hora_fin", "duracion_turno_min"]:
                if campo in data and data[campo] is not None:
                    setattr(horario, campo, data[campo])

            if "id_medico" in data:
                horario.medico = Medico(id=data["id_medico"]) if data["id_medico"] else None

            actualizado = self.repository.modify(horario)
            if not actualizado:
                raise Exception("No se pudo actualizar el horario médico")

            completo = self.repository.get_by_id(horario_id)
            return self._to_dict(completo)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar horario médico")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, horario_id: int):
        try:
            horario = self.repository.get_by_id(horario_id)
            if not horario:
                return None

            eliminado = self.repository.delete(horario)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar horario médico")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, h: HorarioMedico):
        if not h:
            return None

        return {
            "id": h.id,
            "mes": h.mes,
            "anio": h.anio,
            "dia_semana": h.dia_semana,
            "hora_inicio": h.hora_inicio,
            "hora_fin": h.hora_fin,
            "duracion_turno_min": h.duracion_turno_min,
            "medico": {
                "id": h.medico.id if h.medico else None,
                "nombre": getattr(h.medico, "nombre", None),
                "apellido": getattr(h.medico, "apellido", None),
                "matricula": getattr(h.medico, "matricula", None)
            } if h.medico else None
        }

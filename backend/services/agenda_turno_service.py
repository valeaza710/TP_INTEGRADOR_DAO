from flask import jsonify
from datetime import date
from backend.repository.agenda_turno_repository import AgendaTurnoRepository
from backend.clases.agenda_turno import AgendaTurno
from backend.clases.paciente import Paciente
from backend.clases.estado_turno import EstadoTurno
from backend.clases.horario_medico import HorarioMedico


class AgendaTurnoService:
    def __init__(self):
        self.repository = AgendaTurnoRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            agendas = self.repository.get_all()
            return [self._to_dict(a) for a in agendas]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener las agendas")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, agenda_id: int):
        try:
            agenda = self.repository.get_by_id(agenda_id)
            return self._to_dict(agenda) if agenda else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener la agenda")

    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            if not data.get("fecha") or not data.get("hora"):
                raise ValueError("Los campos 'fecha' y 'hora' son obligatorios")

            # ================================
            # ✅ Buscar paciente por DNI
            # ================================
            dni = data.get("dni_paciente")
            if not dni:
                raise ValueError("Debe ingresar el DNI del paciente")

            paciente = self.repository.paciente_repo.get_by_dni(dni)
            if not paciente:
                raise ValueError(f"No existe un paciente con DNI {dni}")

            # ================================
            # ✅ Construir data real
            # ================================
            estado = EstadoTurno(id=data.get("id_estado_turno", 1))
            horario = HorarioMedico(id=data.get("id_horario_medico"))

            nueva = AgendaTurno(
                fecha=data["fecha"],
                hora=data["hora"],
                paciente=paciente,
                estado_turno=estado,
                horario_medico=horario
            )

            guardada = self.repository.save(nueva)
            if not guardada:
                raise Exception("No se pudo guardar el turno")

            completa = self.repository.get_by_id(guardada.id)
            return self._to_dict(completa)

        except ValueError as e:
            return jsonify({"error": str(e)}), 404


    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, agenda_id: int, data: dict):
        try:
            agenda = self.repository.get_by_id(agenda_id)
            if not agenda:
                return None

            if "fecha" in data and data["fecha"] is not None:
                agenda.fecha = data["fecha"]
            if "hora" in data and data["hora"] is not None:
                agenda.hora = data["hora"]
            if data.get("id_paciente"):
                agenda.paciente = Paciente(id=data["id_paciente"])
            if data.get("id_estado_turno"):
                agenda.estado_turno = EstadoTurno(id=data["id_estado_turno"])
            if data.get("id_horario_medico"):
                agenda.horario_medico = HorarioMedico(id=data["id_horario_medico"])

            actualizada = self.repository.modify(agenda)
            if not actualizada:
                raise Exception("No se pudo actualizar la agenda")

            completa = self.repository.get_by_id(agenda_id)
            return self._to_dict(completa)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar la agenda")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, agenda_id: int):
        try:
            agenda = self.repository.get_by_id(agenda_id)
            if not agenda:
                return None

            eliminado = self.repository.delete(agenda)
            return eliminado
        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar la agenda")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, a: AgendaTurno):
        if not a:
            return None

        return {
            "id": a.id,
            "fecha": a.fecha,
            "hora": a.hora,
            "id_paciente": getattr(a.paciente, "id", None),
            "id_estado_turno": getattr(a.estado_turno, "id", None),
            "id_horario_medico": getattr(a.horario_medico, "id", None)
        }

    # ------------------------------------------------------------
    # Ver turnos por médico
    # ------------------------------------------------------------
    def get_by_medico(self, id_medico: int):
        """
        Devuelve los turnos de un médico, excluyendo estados 1, 4 y 5.
        """
        try:
            turnos = self.repository.get_by_medico(id_medico)
            return [self._to_dict(t) for t in turnos]
        except Exception as e:
            print(f"❌ Error en get_by_medico: {e}")
            raise Exception("Error al obtener turnos del médico")

    # ------------------------------------------------------------
    # Ver turnos ya atendidos por médico (historial)
    # ------------------------------------------------------------
    def get_historial_by_medico(self, id_medico: int):
        """
        Devuelve los turnos atendidos (estado = 3) del médico.
        """
        try:
            turnos = self.repository.get_atendidos_by_medico(id_medico)
            return [self._to_dict(t) for t in turnos]
        except Exception as e:
            print(f"❌ Error en get_historial_by_medico: {e}")
            raise Exception("Error al obtener el historial del médico")

    # ------------------------------------------------------------
    # Ver turnos del día actual por médico
    # ------------------------------------------------------------
    def get_turnos_hoy_by_medico(self, id_medico: int):
        """
        Devuelve los turnos del día actual del médico.
        """
        try:
            print(f"⚙️ [SERVICE] Consultando turnos para médico ID={id_medico}")
            turnos = self.repository.get_turnos_hoy_by_medico(id_medico)
            print(f"✅ [SERVICE] Turnos obtenidos: {len(turnos)}")
            return [self._to_dict(t) for t in turnos]

        except Exception as e:
            print(f"❌ Error en get_turnos_hoy_by_medico (service): {e}")
            raise Exception("Error al obtener los turnos de hoy del médico")


    # ------------------------------------------------------------
    # Convertir turno a diccionario
    # ------------------------------------------------------------
    def _to_dict(self, a):
        if not a:
            return None

        return {
            "id": a.id,
            "fecha": str(a.fecha),
            "hora": str(a.hora),
            "paciente": {
                "id": a.paciente.id,
                "nombre": a.paciente.nombre,
                "dni": a.paciente.dni
            } if a.paciente else None,
            "estado_turno": {
                "id": a.estado_turno.id,
                "estado": a.estado_turno.nombre
            } if a.estado_turno else None,
            "horario_medico": {
                "id": a.horario_medico.id,
                "hora_inicio": str(a.horario_medico.hora_inicio),
                "hora_fin": str(a.horario_medico.hora_fin),
                "medico": {
                    "id": a.horario_medico.medico.id,
                    "nombre": a.horario_medico.medico.nombre
                }
            } if a.horario_medico else None
        }

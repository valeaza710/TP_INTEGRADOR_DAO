from flask import jsonify
from backend.repository.agenda_turno_repository import AgendaTurnoRepository
from backend.clases.agenda_turno import AgendaTurno
from backend.clases.paciente import Paciente
from backend.clases.estado_turno import EstadoTurno
from backend.clases.horario_medico import HorarioMedico
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.paciente_repository import PacienteRepository # Necesitas PacienteRepository
# 🚨 IMPORTANTE: Necesitas un PacienteRepository para buscar por ID
from backend.repository.paciente_repository import PacienteRepository 
# 🚨 Asumiendo que PacienteRepository tiene get_by_id


class AgendaTurnoService:
    def __init__(self):
        self.repository = AgendaTurnoRepository()
        self.paciente_repo = PacienteRepository()
        

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


    # CREATE (Ahora es RESERVA/UPDATE)
    # ------------------------------------
    def create(self, data: dict):
        try:
            # 1. Obtener IDs clave del Frontend
            id_agenda = data.get("id_turno") # 🚨 Clave que viene del Frontend
            id_paciente = data.get("id_paciente") # 🚨 Clave que viene del Frontend
            
            if not id_agenda:
                raise ValueError("El ID del turno/slot es obligatorio para reservar.")
            if not id_paciente:
                raise ValueError("El ID del paciente es obligatorio.")

            # 2. Buscar paciente por ID (usando el repo.get_by_id del paciente)
            # 🚨 Necesitas PacienteRepository.get_by_id(id)
            paciente = self.paciente_repo.get_by_id(id_paciente)
            if not paciente:
                return jsonify({"error": f"No existe un paciente con ID {id_paciente}"}), 404
            
            # 3. Obtener el Slot (registro de AgendaTurno) existente
            agenda = self.repository.get_by_id(id_agenda)
            
            if not agenda:
                return jsonify({"error": f"El turno con ID {id_agenda} no fue encontrado."}), 404

            # 4. Verificar que esté Disponible (estado 1)
            if getattr(agenda.estado_turno, "id", None) != 1:
                return jsonify({"error": "El turno ya no está disponible."}), 400

            # 5. ACTUALIZAR el Slot
            agenda.paciente = paciente 
            agenda.estado_turno = EstadoTurno(id=2) # 🚨 CAMBIO DE ESTADO A 2 (Reservado)
            
            guardada = self.repository.modify(agenda) # Usamos modify, no save
            
            if not guardada:
                raise Exception("No se pudo reservar/actualizar el turno")

            # 6. Devolver el turno completo y actualizado
            completa = self.repository.get_by_id(guardada.id)
            return self._to_dict(completa)

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"Error al reservar turno: {e}")
            return jsonify({"error": "Error interno al procesar la reserva."}), 500

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

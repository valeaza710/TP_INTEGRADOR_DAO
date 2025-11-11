# backend/services/turno_service.py
from backend.repository.agenda_turno_repository import AgendaTurnoRepository

class TurnoService:
    def __init__(self):
        self.repo = AgendaTurnoRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, id):
        return self.repo.get_by_id(id)

    def create(self, data):
        # Crear objeto AgendaTurno
        from backend.clases.agenda_turno import AgendaTurno
        from backend.clases.paciente import Paciente
        from backend.clases.estado_turno import EstadoTurno
        from backend.clases.horario_medico import HorarioMedico

        agenda = AgendaTurno(
            fecha=data["fecha"],
            hora=data["hora"],
            paciente=Paciente(id=data["id_paciente"]),
            estado_turno=EstadoTurno(id=data["id_estado_turno"]),
            horario_medico=HorarioMedico(id=data["id_horario_medico"])
        )

        return self.repo.save(agenda)

    def delete(self, id):
        turno = self.repo.get_by_id(id)
        if not turno:
            return None
        return self.repo.delete(turno)

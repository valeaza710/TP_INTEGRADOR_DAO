from datetime import date, time
from backend.clases.paciente import Paciente
from backend.clases.estado_turno import EstadoTurno
from backend.clases.horario_medico import HorarioMedico

class AgendaTurno:
    def __init__(
        self,
        id: int = None,
        fecha: date = None,
        hora: time = None,
        paciente: Paciente = None,
        estado_turno: EstadoTurno = None,
        horario_medico: HorarioMedico = None
    ):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.paciente = paciente
        self.estado_turno = estado_turno
        self.horario_medico = horario_medico

    def __repr__(self):
        return (f"AgendaTurno(id={self.id}, fecha={self.fecha}, hora={self.hora}, "
                f"paciente={self.paciente}, estado_turno={self.estado_turno}, "
                f"horario_medico={self.horario_medico})")

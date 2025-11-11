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
    

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": str(self.fecha),
            "hora": str(self.hora),

            "paciente": {
                "id": self.paciente.id,
                "nombre": self.paciente.nombre,
                "apellido": self.paciente.apellido,
                "dni": self.paciente.dni
            } if self.paciente else None,

            "estado_turno": {
                "id": self.estado_turno.id,
                "estado": self.estado_turno.estado
            } if self.estado_turno else None,

            "horario_medico": {
                "id": self.horario_medico.id,
                "consultorio": self.horario_medico.consultorio,
                "medico": {
                    "id": self.horario_medico.medico.id,
                    "nombre": self.horario_medico.medico.nombre,
                    "apellido": self.horario_medico.medico.apellido
                } if self.horario_medico.medico else None,
                "especialidad": {
                    "id": self.horario_medico.medico.especialidades[0].id,
                    "nombre": self.horario_medico.medico.especialidades[0].nombre
                } if (self.horario_medico.medico and self.horario_medico.medico.especialidades) else None
            } if self.horario_medico else None,
        }


from backend.clases.historial_clinico import HistorialClinico
from backend.clases.agenda_turno import AgendaTurno

class Visita:
    def __init__(
        self,
        id: int = None,
        historial_clinico: HistorialClinico = None,
        turno: AgendaTurno = None,
        comentario: str = ""
    ):
        self.id = id
        self.historial_clinico = historial_clinico
        self.turno = turno
        self.comentario = comentario

    def __repr__(self):
        hid = self.historial_clinico.id if self.historial_clinico else None
        aid = self.turno.id if self.turno else None
        return f"Visita(id={self.id}, historial_clinico_id={hid}, turno_id={aid}, comentario='{self.comentario}')"

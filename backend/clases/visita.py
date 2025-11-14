from backend.clases.historial_clinico import HistorialClinico
from backend.clases.agenda_turno import AgendaTurno

class Visita:
    def __init__(
        self,
        id: int = None,
        historial_clinico: HistorialClinico = None,
        agenda_turno: AgendaTurno = None,
        comentario: str = ""
    ):
        self.id = id
        self.historial_clinico = historial_clinico
        self.agenda_turno = agenda_turno
        self.comentario = comentario

    def __repr__(self):
        hid = self.historial_clinico.id if self.historial_clinico else None
        aid = self.agenda_turno.id if self.agenda_turno else None
        return f"Visita(id={self.id}, historial_clinico_id={hid}, turno_id={aid}, comentario='{self.comentario}')"

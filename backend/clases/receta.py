from datetime import date
from backend.clases.enfermedad import Enfermedad
from backend.clases.visita import Visita
from backend.clases.paciente import Paciente

class Receta:
    def __init__(
        self,
        id: int = None,
        visita: Visita = None,
        paciente: Paciente = None,
        descripcion: str = "",
        fecha_emision: date = None,
        enfermedad: Enfermedad = None
    ):
        self.id = id
        self.visita = visita
        self.paciente = paciente
        self.descripcion = descripcion
        self.fecha_emision = fecha_emision or date.today()  # Por defecto, hoy
        self.enfermedad = enfermedad

    def __repr__(self):
        vid = self.visita.id if self.visita else None
        pid = self.paciente.id if self.paciente else None
        return (f"Receta(id={self.id}, visita_id={vid}, paciente_id={pid}, "
                f"descripcion='{self.descripcion}', fecha_emision={self.fecha_emision})")
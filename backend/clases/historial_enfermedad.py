from datetime import date
from backend.clases.historial_clinico import HistorialClinico
from backend.clases.enfermedad import Enfermedad


class HistorialEnfermedad:
    def __init__(
        self,
        historial_clinico: HistorialClinico = None,
        enfermedad: Enfermedad = None,
        fecha_diagnostico: date = None,
        observaciones: str = None
    ):
        self.id = id
        self.historial_clinico = historial_clinico
        self.enfermedad = enfermedad
        self.fecha_diagnostico = fecha_diagnostico
        self.observaciones = observaciones

    def __repr__(self):
        return (
            f"HistorialEnfermedad(id={self.id}, historial_clinico={self.historial_clinico}, "
            f"enfermedad={self.enfermedad}, fecha_diagnostico='{self.fecha_diagnostico}', "
            f"observaciones='{self.observaciones}')"
        )

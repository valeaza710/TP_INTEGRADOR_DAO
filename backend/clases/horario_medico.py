from .medico import Medico

class HorarioMedico:
    def __init__(
        self,
        id: int = None,
        medico: Medico = None,
        mes: int = None,
        anio: int = None,
        dia_semana: str = None,
        hora_inicio: str = None,
        hora_fin: str = None,
        duracion_turno_min: int = None
    ):
        self.id = id
        self.medico = medico            # objeto Medico completo
        self.mes = mes
        self.anio = anio
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.duracion_turno_min = duracion_turno_min

    def __repr__(self):
        med_id = self.medico.id if self.medico else None
        return (f"HorarioMedico(id={self.id}, medico_id={med_id}, mes={self.mes}, anio={self.anio}, "
                f"dia_semana='{self.dia_semana}', {self.hora_inicio}-{self.hora_fin}, duracion={self.duracion_turno_min})")

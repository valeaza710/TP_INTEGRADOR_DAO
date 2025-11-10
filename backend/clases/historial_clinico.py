from backend.clases.paciente import Paciente

class HistorialClinico:
    def __init__(
        self,
        id: int = None,
        paciente: Paciente = None,
        peso: float = 0.0,
        altura: float = 0.0,
        grupo_sanguineo: str = ""
    ):
        self.id = id
        self.paciente = paciente        # objeto Paciente o None
        self.peso = peso
        self.altura = altura
        self.grupo_sanguineo = grupo_sanguineo

    def __repr__(self):
        pid = self.paciente.id if (self.paciente and hasattr(self.paciente, "id")) else None
        return (f"HistorialClinico(id={self.id}, paciente_id={pid}, "
                f"peso={self.peso}, altura={self.altura}, grupo_sanguineo='{self.grupo_sanguineo}')")

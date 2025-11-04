class Enfermedad:
    def __init__(
        self,
        id: int = None,
        nombre: str = "",
        descripcion: str = None
    ):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return f"Enfermedad(id={self.id}, nombre='{self.nombre}', descripcion='{self.descripcion}')"

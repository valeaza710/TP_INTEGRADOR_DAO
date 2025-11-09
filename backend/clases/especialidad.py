class Especialidad:
    def __init__(self, id: int = None, nombre: str = None):
        self.id = id
        self.nombre = nombre

    def __repr__(self):
        return f"Especialidad(id={self.id}, nombre='{self.nombre}')"


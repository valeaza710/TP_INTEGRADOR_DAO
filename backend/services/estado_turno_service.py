from repository.estado_turno_repository import EstadoTurnoRepository
from clases.estado_turno import EstadoTurno

class EstadoTurnoService:
    def __init__(self):
        self.repo = EstadoTurnoRepository()

    def create(self, data: dict):
        """Crea un nuevo estado de turno"""
        if not data.get("nombre"):
            raise ValueError("El campo 'nombre' es obligatorio")

        estado = EstadoTurno(nombre=data["nombre"])
        return self.repo.save(estado)

    def get_all(self):
        """Obtiene todos los estados"""
        return self.repo.get_all()

    def get_by_id(self, estado_id: int):
        """Obtiene un estado por ID"""
        return self.repo.get_by_id(estado_id)

    def update(self, estado_id: int, data: dict):
        """Modifica un estado existente"""
        estado = self.repo.get_by_id(estado_id)
        if not estado:
            return None

        if "nombre" in data:
            estado.nombre = data["nombre"]

        return self.repo.modify(estado)

    def delete(self, estado_id: int):
        """Elimina un estado"""
        estado = self.repo.get_by_id(estado_id)
        if not estado:
            return None

        return self.repo.delete(estado)

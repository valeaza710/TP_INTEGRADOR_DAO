from backend.repository.visita_repository import VisitaRepository
from backend.clases.visita import Visita
from backend.clases.historial_clinico import HistorialClinico
from backend.clases.agenda_turno import AgendaTurno

class VisitaService:
    def __init__(self):
        self.repository = VisitaRepository()

    # ---------------------------------
    # GET ALL
    # ---------------------------------
    def get_all(self):
        try:
            visitas = self.repository.get_all()
            return [self._to_dict(v) for v in visitas]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener visitas")

    # ---------------------------------
    # GET BY ID
    # ---------------------------------
    def get_by_id(self, visita_id: int):
        try:
            visita = self.repository.get_by_id(visita_id)
            return self._to_dict(visita) if visita else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener visita")

    # ---------------------------------
    # CREATE
    # ---------------------------------
    def create(self, data: dict):
        try:
            # Validaciones
            if not data.get("id_historial_clinico"):
                raise ValueError("El ID del historial clínico es obligatorio")

            if not data.get("id_turno"):
                raise ValueError("El ID del turno es obligatorio")

            comentario = data.get("comentario", "")

            # Crear objetos mínimos
            historial = HistorialClinico(id=data["id_historial_clinico"])
            turno = AgendaTurno(id=data["id_turno"])

            visita = Visita(
                historial_clinico=historial,
                turno=turno,
                comentario=comentario
            )

            guardada = self.repository.save(visita)
            if not guardada:
                raise Exception("No se pudo guardar la visita")

            return self._to_dict(guardada)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear visita")

    # ---------------------------------
    # UPDATE
    # ---------------------------------
    def update(self, visita_id: int, data: dict):
        try:
            visita = self.repository.get_by_id(visita_id)
            if not visita:
                return None

            # Actualizar campos
            if "id_historial_clinico" in data:
                visita.historial_clinico = HistorialClinico(id=data["id_historial_clinico"])

            if "id_turno" in data:
                visita.turno = AgendaTurno(id=data["id_turno"])

            if "comentario" in data:
                visita.comentario = data["comentario"]

            actualizada = self.repository.modify(visita)
            if not actualizada:
                raise Exception("No se pudo actualizar la visita")

            return self._to_dict(actualizada)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar visita")

    # ---------------------------------
    # DELETE
    # ---------------------------------
    def delete(self, visita_id: int):
        try:
            visita = self.repository.get_by_id(visita_id)
            if not visita:
                return None

            eliminado = self.repository.delete(visita)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar visita")

    # ---------------------------------
    # SERIALIZER
    # ---------------------------------
    def _to_dict(self, v: Visita):
        if not v:
            return None

        return {
            "id": v.id,
            "comentario": v.comentario,
            "historial_clinico": {
                "id": v.historial_clinico.id
            } if v.historial_clinico else None,
            "turno": {
                "id": v.turno.id
            } if v.turno else None
        }

from backend.repository.historial_enfermedad_repository import HistorialEnfermedadRepository
from backend.clases.historial_enfermedad import HistorialEnfermedad
from backend.clases.historial_clinico import HistorialClinico
from backend.clases.enfermedad import Enfermedad

class HistorialEnfermedadService:
    def __init__(self):
        self.repository = HistorialEnfermedadRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            historial = self.repository.get_all()
            return [self._to_dict(h) for h in historial]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener historiales de enfermedad")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, historial_id: int):
        try:
            h = self.repository.get_by_id(historial_id)
            return self._to_dict(h) if h else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener historial de enfermedad")

    # ------------------------------------
    # GET BY PACIENTE
    # ------------------------------------
    def get_by_paciente(self, id_paciente: int):
        try:
            historiales = self.repository.get_by_paciente(id_paciente)
            if not historiales:
                return []

            return [self._to_dict(h) for h in historiales]

        except Exception as e:
            print(f"Error en get_by_paciente: {e}")
            raise Exception("Error al obtener historiales de enfermedad por paciente")

    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            # Validaciones básicas
            if not data.get("historial_clinico_id"):
                raise ValueError("El campo 'historial_clinico_id' es obligatorio")
            if not data.get("enfermedad_id"):
                raise ValueError("El campo 'enfermedad_id' es obligatorio")
            if not data.get("fecha_diagnostico"):
                raise ValueError("El campo 'fecha_diagnostico' es obligatorio")

            nuevo_historial = HistorialEnfermedad(
                historial_clinico=HistorialClinico(id=data["historial_clinico_id"]),
                enfermedad=Enfermedad(id=data["enfermedad_id"]),
                fecha_diagnostico=data["fecha_diagnostico"],
                observaciones=data.get("observaciones", "")
            )

            guardado = self.repository.save(nuevo_historial)
            if not guardado:
                raise Exception("No se pudo guardar el historial de enfermedad")

            completo = self.repository.get_by_id(guardado.id)
            return self._to_dict(completo)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear historial de enfermedad")

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, historial_id: int, data: dict):
        try:
            historial = self.repository.get_by_id(historial_id)
            if not historial:
                return None

            if "enfermedad_id" in data:
                historial.enfermedad = Enfermedad(id=data["enfermedad_id"])
            if "fecha_diagnostico" in data:
                historial.fecha_diagnostico = data["fecha_diagnostico"]
            if "observaciones" in data:
                historial.observaciones = data["observaciones"]

            actualizado = self.repository.modify(historial)

            if not actualizado:
                raise Exception("No se pudo actualizar el historial de enfermedad")

            completo = self.repository.get_by_id(historial_id)

            return self._to_dict(completo)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar historial de enfermedad")

    # ------------------------------------
    # DELETE
    # ------------------------------------
    def delete(self, historial_id: int):
        try:
            historial = self.repository.get_by_id(historial_id)
            if not historial:
                return None

            eliminado = self.repository.delete(historial)
            return eliminado

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar historial de enfermedad")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, h: HistorialEnfermedad):

        return {
            "id": h.id,

            # Datos del historial clínico y del paciente asociado
            "historial_clinico": {
                "id": h.historial_clinico.id if h.historial_clinico else None,
                "peso": getattr(h.historial_clinico, "peso", None),
                "altura": getattr(h.historial_clinico, "altura", None),
                "grupo_sanguineo": getattr(h.historial_clinico, "grupo_sanguineo", None),
                "paciente_id": getattr(h.historial_clinico.paciente, "id", None),
            } if h.historial_clinico else None,

            # Datos completos de la enfermedad
            "enfermedad": {
                "id": getattr(h.enfermedad, "id", None),
                "nombre": getattr(h.enfermedad, "nombre", None),
                "descripcion": getattr(h.enfermedad, "descripcion", None)
            } if h.enfermedad else None,

            "fecha_diagnostico": h.fecha_diagnostico,
            "observaciones": h.observaciones
        }




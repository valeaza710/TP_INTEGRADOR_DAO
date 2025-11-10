from repository.historial_clinico_repository import HistorialClinicoRepository
from repository.paciente_repository import PacienteRepository
from clases.historial_clinico import HistorialClinico
from clases.paciente import Paciente


class HistorialClinicoService:
    def __init__(self):
        self.repository = HistorialClinicoRepository()
        self.paciente_repository = PacienteRepository()

    # ------------------------------------
    # GET ALL
    # ------------------------------------
    def get_all(self):
        try:
            historiales = self.repository.get_all()
            return [self._to_dict(h) for h in historiales]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener historiales clínicos")

    # ------------------------------------
    # GET BY ID
    # ------------------------------------
    def get_by_id(self, historial_id: int):
        try:
            historial = self.repository.get_by_id(historial_id)
            return self._to_dict(historial) if historial else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener historial clínico")

    # ------------------------------------
    # CREATE
    # ------------------------------------
    def create(self, data: dict):
        try:
            if not data.get("id_paciente"):
                raise ValueError("El campo 'id_paciente' es obligatorio")

            paciente = self.paciente_repository.get_by_id(data["id_paciente"])
            if not paciente:
                raise ValueError("El paciente especificado no existe")

            nuevo_historial = HistorialClinico(
                paciente=paciente,
                peso=float(data.get("peso", 0.0)),
                altura=float(data.get("altura", 0.0)),
                grupo_sanguineo=data.get("grupo_sanguineo", "")
            )

            guardado = self.repository.save(nuevo_historial)
            if not guardado:
                raise Exception("No se pudo guardar el historial clínico")

            completo = self.repository.get_by_id(guardado.id)
            return self._to_dict(completo)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear historial clínico")

    # ------------------------------------
    # UPDATE
    # ------------------------------------
    def update(self, historial_id: int, data: dict):
        try:
            historial = self.repository.get_by_id(historial_id)
            if not historial:
                return None

            for campo in ["peso", "altura", "grupo_sanguineo"]:
                if campo in data and data[campo] is not None:
                    setattr(historial, campo, data[campo])

            if "id_paciente" in data:
                paciente = self.paciente_repository.get_by_id(data["id_paciente"])
                if not paciente:
                    raise ValueError("El paciente especificado no existe")
                historial.paciente = paciente

            actualizado = self.repository.modify(historial)
            if not actualizado:
                raise Exception("No se pudo actualizar el historial clínico")

            completo = self.repository.get_by_id(historial_id)
            return self._to_dict(completo)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al actualizar historial clínico")

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
            raise Exception("Error al eliminar historial clínico")

    # ------------------------------------
    # SERIALIZADOR
    # ------------------------------------
    def _to_dict(self, h: HistorialClinico):
        if not h:
            return None

        return {
            "id": h.id,
            "peso": h.peso,
            "altura": h.altura,
            "grupo_sanguineo": h.grupo_sanguineo,
            "paciente": {
                "id": h.paciente.id if h.paciente else None,
                "nombre": getattr(h.paciente, "nombre", None),
                "apellido": getattr(h.paciente, "apellido", None),
                "dni": getattr(h.paciente, "dni", None)
            } if h.paciente else None
        }

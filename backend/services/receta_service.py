from repository.receta_repository import RecetaRepository
from clases.receta import Receta
from clases.visita import Visita
from clases.paciente import Paciente
from datetime import date

class RecetaService:
    def __init__(self):
        self.repository = RecetaRepository()

    # -------------------------------
    # GET ALL
    # -------------------------------
    def get_all(self):
        try:
            recetas = self.repository.get_all()
            return [self._to_dict(r) for r in recetas]
        except Exception as e:
            print(f"Error en get_all: {e}")
            raise Exception("Error al obtener recetas")

    # -------------------------------
    # GET BY ID
    # -------------------------------
    def get_by_id(self, receta_id: int):
        try:
            receta = self.repository.get_by_id(receta_id)
            return self._to_dict(receta) if receta else None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            raise Exception("Error al obtener la receta")

    # -------------------------------
    # CREATE
    # -------------------------------
    def create(self, data: dict):
        try:
            # Validaciones
            if not data.get("descripcion") or data["descripcion"].strip() == "":
                raise ValueError("La descripción es obligatoria")

            if not data.get("id_paciente"):
                raise ValueError("El ID del paciente es obligatorio")

            if not data.get("id_visita"):
                raise ValueError("El ID de la visita es obligatorio")

            # Crear entidades mínimas
            paciente = Paciente(id=data["id_paciente"])
            visita = Visita(id=data["id_visita"])

            fecha = data.get("fecha_emision") or date.today()

            nueva = Receta(
                visita=visita,
                paciente=paciente,
                descripcion=data["descripcion"],
                fecha_emision=fecha
            )

            guardada = self.repository.save(nueva)
            if not guardada:
                raise Exception("No se pudo guardar la receta")

            return self._to_dict(guardada)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create: {e}")
            raise Exception("Error al crear la receta")

    # -------------------------------
    # UPDATE
    # -------------------------------
    def update(self, receta_id: int, data: dict):
        try:
            receta = self.repository.get_by_id(receta_id)
            if not receta:
                return None

            # Actualizar campos
            if "descripcion" in data and data["descripcion"].strip():
                receta.descripcion = data["descripcion"]

            if "id_paciente" in data:
                receta.paciente = Paciente(id=data["id_paciente"])

            if "id_visita" in data:
                receta.visita = Visita(id=data["id_visita"])

            if "fecha_emision" in data:
                receta.fecha_emision = data["fecha_emision"]

            actualizada = self.repository.modify(receta)
            if not actualizada:
                raise Exception("No se pudo actualizar la receta")

            return self._to_dict(actualizada)

        except Exception as e:
            print(f"Error en update: {e}")
            raise Exception("Error al modificar la receta")

    # -------------------------------
    # DELETE
    # -------------------------------
    def delete(self, receta_id: int):
        try:
            receta = self.repository.get_by_id(receta_id)
            if not receta:
                return None

            return self.repository.delete(receta)

        except Exception as e:
            print(f"Error en delete: {e}")
            raise Exception("Error al eliminar la receta")

    # -------------------------------
    # SERIALIZADOR
    # -------------------------------
    def _to_dict(self, r: Receta):
        if not r:
            return None

        return {
            "id": r.id,
            "descripcion": r.descripcion,
            "fecha_emision": str(r.fecha_emision),
            "visita": {
                "id": r.visita.id
            } if r.visita else None,
            "paciente": {
                "id": r.paciente.id
            } if r.paciente else None
        }


    def get_by_paciente(self, id_paciente: int):
        try:
            recetas = self.repository.get_by_paciente(id_paciente)
            return [self._to_dict(r) for r in recetas]
        except Exception as e:
            print(f"Error en get_by_paciente: {e}")
            raise Exception("Error al obtener recetas por paciente")
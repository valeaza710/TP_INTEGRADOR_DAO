from backend.clases.agenda_turno import AgendaTurno
from backend.clases.historial_clinico import HistorialClinico
from backend.repository.agenda_turno_repository import AgendaTurnoRepository
from backend.repository.historial_clinico_repository import HistorialClinicoRepository
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.receta_repository import RecetaRepository
from backend.clases.receta import Receta
from backend.clases.visita import Visita
from backend.clases.enfermedad import Enfermedad
from backend.clases.paciente import Paciente
from datetime import date

from backend.repository.visita_repository import VisitaRepository


class RecetaService:
    def __init__(self):
        self.agenda_repo = AgendaTurnoRepository()
        self.visita_repository = VisitaRepository()
        self.historial_repository = HistorialClinicoRepository()
        self.paciente_repository = PacienteRepository()
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

            # Si viene enfermedad desde el front, se crea solo con ID
            enfermedad = None
            if data.get("id_enfermedad"):
                enfermedad = Enfermedad(id=data["id_enfermedad"])

            nueva = Receta(
                visita=visita,
                paciente=paciente,
                descripcion=data["descripcion"],
                fecha_emision=fecha,
                enfermedad=enfermedad
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
                "id": r.visita.id,
                "medico_nombre": r.visita.turno.horario_medico.medico,
                "medico_apellido": r.visita.turno.horario_medico.medico
            } if r.visita else None,
            "paciente": {
                "id": r.paciente.id,
                "nombre": r.paciente.nombre,
                "apellido": r.paciente.apellido,
                "dni": r.paciente.dni,
                "edad": r.paciente.edad,
                "fecha_nacimiento": r.paciente.fecha_nacimiento,
                "mail": r.paciente.mail,
            } if r.paciente else None,
            "enfermedad": {
                "id": r.enfermedad.id,
                "nombre": r.enfermedad.nombre,
                "descripcion": r.enfermedad.descripcion,
            } if r.enfermedad else None,
        }

    def create_from_front(self, data: dict):
        try:
            print("Datos recibidos:", data)

            # Validaciones básicas
            if not data.get("dni_paciente"):
                raise ValueError("El DNI del paciente es obligatorio")
            if not data.get("medico_id"):
                raise ValueError("El ID del médico es obligatorio")
            if not data.get("id_agenda_turno"):
                raise ValueError("El ID del turno es obligatorio")

            # Convertir IDs a enteros
            medico_id = int(data["medico_id"])
            id_agenda_turno = int(data["id_agenda_turno"])
            enfermedad_id = int(data["enfermedad_id"]) if data.get("enfermedad_id") else None

            # Buscar o crear paciente
            paciente = self.paciente_repository.get_by_dni(data["dni_paciente"])[0]
            if not paciente:
                paciente = Paciente(dni=data["dni_paciente"])
                paciente = self.paciente_repository.save(paciente)

            # Crear historial clínico si no existe
            historial = self.historial_repository.get_by_paciente(id_paciente=paciente.id)
            if not historial:
                historailaa = HistorialClinico(paciente=paciente)
                historial = self.historial_repository.save(historailaa)
            historial_id = historial.id


            # Obtener turno
            agenda_turno = self.agenda_repo.get_by_id(id_agenda_turno)
            if not agenda_turno:
                raise ValueError(f"No se encontró el turno con ID {id_agenda_turno}")
            agenda_turno_id = agenda_turno.id

            # Crear visita con los comentarios (observaciones)
            visita = {
                "comentario": data.get("observaciones", ""),
                "turno_id": agenda_turno_id,
                "historial_clinico_id": historial_id,
            }

            visita = self.visita_repository.save(visita)

            # Preparar descripción de la receta a partir de los medicamentos
            medicamentos_str = ", ".join([m["nombre"] for m in data.get("medicamentos", []) if m.get("nombre")])

            # Crear receta
            enfermedad = Enfermedad(id=enfermedad_id) if enfermedad_id else None

            receta = Receta(
                visita=visita,
                paciente=paciente,
                descripcion=medicamentos_str,
                fecha_emision=date.today(),
                enfermedad=enfermedad
            )
            receta = self.repository.save(receta)

            visita_pro = Visita(
                historial_clinico = receta.visita.get("historial_clinico_id"),
                agenda_turno = receta.visita.get("turno_id"),
                comentario = receta.visita.get("comentario"),
                id = receta.visita.get("id")
            )

            receta.visita = visita_pro

            return self._to_dict2(receta)

        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error en create_from_front: {e}")
            raise Exception("Error al crear la receta desde el front")


    def _to_dict2(self, r: Receta):
        if not r:
            return None

        return {
            "id": r.id,
            "descripcion": r.descripcion,
            "fecha_emision": str(r.fecha_emision),
            "paciente": {
                "id": r.paciente.id,
                "nombre": r.paciente.nombre,
                "apellido": r.paciente.apellido,
                "dni": r.paciente.dni,
            } if r.paciente else None,
            "enfermedad": {
                "id": r.enfermedad.id,
                "nombre": r.enfermedad.nombre,
                "descripcion": r.enfermedad.descripcion,
            } if r.enfermedad else None,
        }
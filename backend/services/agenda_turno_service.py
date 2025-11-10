from clases.agenda_turno import AgendaTurno
from clases.paciente import Paciente
from clases.estado_turno import EstadoTurno
from clases.horario_medico import HorarioMedico
from repository.agenda_turno_repository import AgendaTurnoRepository

class AgendaTurnoService:
    def __init__(self):
        self.repo = AgendaTurnoRepository()

    def crear_agenda(self, data):
        """
        Crea un nuevo turno en la agenda a partir de un diccionario (JSON del body).
        """
        try:
            paciente = Paciente(id=data.get("id_paciente")) if data.get("id_paciente") else None
            estado = EstadoTurno(id=data.get("id_estado_turno")) if data.get("id_estado_turno") else None
            horario = HorarioMedico(id=data.get("id_horario_medico")) if data.get("id_horario_medico") else None

            agenda = AgendaTurno(
                fecha=data.get("fecha"),
                hora=data.get("hora"),
                paciente=paciente,
                estado_turno=estado,
                horario_medico=horario
            )
            return self.repo.save(agenda)
        except Exception as e:
            print(f"Error en crear_agenda: {e}")
            return None

    def obtener_todos(self):
        return self.repo.get_all()

    def obtener_por_id(self, agenda_id):
        return self.repo.get_by_id(agenda_id)

    def modificar(self, agenda_id, data):
        agenda = self.repo.get_by_id(agenda_id)
        if not agenda:
            return None

        agenda.fecha = data.get("fecha", agenda.fecha)
        agenda.hora = data.get("hora", agenda.hora)

        if data.get("id_paciente"):
            agenda.paciente = Paciente(id=data.get("id_paciente"))
        if data.get("id_estado_turno"):
            agenda.estado_turno = EstadoTurno(id=data.get("id_estado_turno"))
        if data.get("id_horario_medico"):
            agenda.horario_medico = HorarioMedico(id=data.get("id_horario_medico"))

        return self.repo.modify(agenda)

    def eliminar(self, agenda_id):
        agenda = self.repo.get_by_id(agenda_id)
        if not agenda:
            return False
        return self.repo.delete(agenda)

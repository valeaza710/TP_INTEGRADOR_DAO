from backend.data_base.connection import DataBaseConnection
from backend.clases.agenda_turno import AgendaTurno
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.estado_turno_repository import EstadoTurnoRepository
from backend.repository.horario_medico_repository import HorarioMedicoRepository
from backend.repository.repository import Repository

class AgendaTurnoRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()
        self.paciente_repo = PacienteRepository()
        self.estado_repo = EstadoTurnoRepository()
        self.horario_repo = HorarioMedicoRepository()

    def save(self, agenda: AgendaTurno):
        query = """
            INSERT INTO agenda_turno (fecha, hora, id_paciente, id_estado_turno, id_horario_medico)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            agenda.fecha,
            agenda.hora,
            agenda.paciente.id if agenda.paciente else None,
            agenda.estado_turno.id if agenda.estado_turno else None,
            agenda.horario_medico.id if agenda.horario_medico else None,
        )

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            agenda.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return agenda
        except Exception as e:
            print(f"❌ Error al guardar agenda_turno: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_by_id(self, agenda_id: int):
        query = "SELECT * FROM agenda_turno WHERE id = ?"
        data = self.db.execute_query(query, (agenda_id,), fetch=True)
        if not data:
            return None
        row = data[0]

        paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row["id_paciente"] else None
        estado = self.estado_repo.get_by_id(row["id_estado_turno"]) if row["id_estado_turno"] else None
        horario = self.horario_repo.get_by_id(row["id_horario_medico"]) if row["id_horario_medico"] else None

        return AgendaTurno(
            id=row["id"],
            fecha=row["fecha"],
            hora=row["hora"],
            paciente=paciente,
            estado_turno=estado,
            horario_medico=horario
        )

    def get_all(self):
        query = "SELECT * FROM agenda_turno"
        data = self.db.execute_query(query, fetch=True)
        agendas = []

        if data:
            for row in data:
                paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row["id_paciente"] else None
                estado = self.estado_repo.get_by_id(row["id_estado_turno"]) if row["id_estado_turno"] else None
                horario = self.horario_repo.get_by_id(row["id_horario_medico"]) if row["id_horario_medico"] else None

                agendas.append(AgendaTurno(
                    id=row["id"],
                    fecha=row["fecha"],
                    hora=row["hora"],
                    paciente=paciente,
                    estado_turno=estado,
                    horario_medico=horario
                ))

        return agendas

    def modify(self, agenda: AgendaTurno):
        query = """
            UPDATE agenda_turno
            SET fecha = ?, hora = ?, id_paciente = ?, id_estado_turno = ?, id_horario_medico = ?
            WHERE id = ?
        """
        params = (
            agenda.fecha,
            agenda.hora,
            agenda.paciente.id if agenda.paciente else None,
            agenda.estado_turno.id if agenda.estado_turno else None,
            agenda.horario_medico.id if agenda.horario_medico else None,
            agenda.id
        )

        success = self.db.execute_query(query, params)
        return agenda if success else None

    def delete(self, agenda: AgendaTurno):
        query = "DELETE FROM agenda_turno WHERE id = ?"
        success = self.db.execute_query(query, (agenda.id,))
        return success

# ------------------------------------------------------------
    # Obtener todos los turnos de un médico (excepto estados 1, 4, 5)
    # ------------------------------------------------------------
    def get_by_medico(self, id_medico: int):
        """
        Devuelve todos los turnos asociados a un médico,
        excluyendo los estados 1, 4 y 5.
        """
        query = """
            SELECT a.*
            FROM agenda_turno a
            JOIN horario_medico h ON a.id_horario_medico = h.id
            WHERE h.id_medico = ?
              AND a.id_estado_turno NOT IN (1, 4, 5)
            ORDER BY a.fecha, a.hora
        """

        rows = self.db.execute_query(query, (id_medico,), fetch=True)
        if not rows:
            return []

        turnos = []
        for r in rows:
            turno = self._map_row_to_agenda_turno(r)
            turnos.append(turno)
        return turnos

    #PARA PODER MANEJAR LOS DATOS EN FORMATO JSON
    def _to_dict(self, a: AgendaTurno):
        if not a:
            return None

        return {
            "id": a.id,
            "fecha": str(a.fecha),
            "hora": str(a.hora),

            # Paciente completo
            "paciente": {
                "id": a.paciente.id,
                "nombre": a.paciente.nombre,
                "dni": a.paciente.dni
            } if a.paciente else None,

            # Estado turno
            "estado_turno": {
                "id": a.estado_turno.id,
                "estado": a.estado_turno.estado
            } if a.estado_turno else None,

            # Horario + información del médico
            "horario_medico": {
                "id": a.horario_medico.id,
                "hora_inicio": str(a.horario_medico.hora_inicio),
                "hora_fin": str(a.horario_medico.hora_fin),
                "medico": {
                    "id": a.horario_medico.medico.id,
                    "nombre": a.horario_medico.medico.nombre,
                    "especialidad": a.horario_medico.medico.especialidad.nombre
                }
            } if a.horario_medico else None
    }

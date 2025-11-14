from backend.data_base.connection import DataBaseConnection
from backend.clases.agenda_turno import AgendaTurno
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.estado_turno_repository import EstadoTurnoRepository
from backend.repository.horario_medico_repository import HorarioMedicoRepository
from backend.repository.repository import Repository
from datetime import date


class AgendaTurnoRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()
        self.paciente_repo = PacienteRepository()
        self.estado_repo = EstadoTurnoRepository()
        self.horario_repo = HorarioMedicoRepository()

    # -------------------------------------------------------------------------
    # Crear un nuevo turno
    # -------------------------------------------------------------------------
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

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            agenda.id = cursor.lastrowid
            return agenda
        except Exception as e:
            print(f"❌ Error al guardar agenda_turno: {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # -------------------------------------------------------------------------
    # Obtener un turno por ID
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Obtener todos los turnos
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Modificar un turno
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Eliminar un turno
    # -------------------------------------------------------------------------
    def delete(self, agenda: AgendaTurno):
        query = "DELETE FROM agenda_turno WHERE id = ?"
        success = self.db.execute_query(query, (agenda.id,))
        return success

    # -------------------------------------------------------------------------
    # Obtener todos los turnos de un médico (excepto estados 1, 4, 5)
    # -------------------------------------------------------------------------
    def get_by_medico(self, id_medico: int):
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

    # -------------------------------------------------------------------------
    # Convertir objeto AgendaTurno a diccionario (para JSON)
    # -------------------------------------------------------------------------
    def _to_dict(self, a: AgendaTurno):
        if not a:
            return None

        return {
            "id": a.id,
            "fecha": str(a.fecha),
            "hora": str(a.hora),
            "paciente": {
                "id": a.paciente.id,
                "nombre": a.paciente.nombre,
                "dni": a.paciente.dni
            } if a.paciente else None,
            "estado_turno": {
                "id": a.estado_turno.id,
                "estado": a.estado_turno.estado
            } if a.estado_turno else None,
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

    # -------------------------------------------------------------------------
    # Ver turnos ya atendidos por médico (historial)
    # -------------------------------------------------------------------------
    def get_atendidos_by_medico(self, id_medico: int):
        """
        Devuelve todos los turnos de un médico que ya fueron atendidos.
        Se asume que el estado 3 = 'Ya atendido' o como sea que se llame.
        """
        query = """
            SELECT a.*
            FROM agenda_turno a
            JOIN horario_medico h ON a.id_horario_medico = h.id
            WHERE h.id_medico = ?
              AND a.id_estado_turno = 3
            ORDER BY a.fecha DESC, a.hora DESC
        """
        rows = self.db.execute_query(query, (id_medico,), fetch=True)
        if not rows:
            return []

        turnos = []
        for r in rows:
            turnos.append(self._map_row_to_agenda_turno(r))
        return turnos

    # -------------------------------------------------------------------------
    # Ver turnos del día actual por médico
    # -------------------------------------------------------------------------
    def get_turnos_hoy_by_medico(self, id_medico: int):
        """
        Devuelve los turnos del día actual de un médico.
        Excluye los estados cancelado (4) y ausente (5).
        """
        hoy = date.today().isoformat()
        query = """
            SELECT a.*
            FROM agenda_turno a
            JOIN horario_medico h ON a.id_horario_medico = h.id
            WHERE h.id_medico = ?
              AND a.fecha = ?
              AND a.id_estado_turno NOT IN (4, 5)
            ORDER BY a.hora ASC
        """
        rows = self.db.execute_query(query, (id_medico, hoy), fetch=True)
        if not rows:
            return []

        turnos = []
        for r in rows:
            turnos.append(self._map_row_to_agenda_turno(r))
        return turnos

#PARA PANEL SECRETARIA
    def get_todos_los_turnos(self):
        query = """
            SELECT 
                a.id,
                a.fecha,
                a.hora,
                p.dni AS dni_paciente,
                p.nombre AS nombre_paciente,
                p.apellido AS apellido_paciente,
                m.nombre AS nombre_medico,
                m.apellido AS apellido_medico,
                et.nombre AS estado
            FROM agenda_turno a
            LEFT JOIN paciente p ON a.id_paciente = p.id
            LEFT JOIN horario_medico hm ON a.id_horario_medico = hm.id
            LEFT JOIN medico m ON hm.id_medico = m.id
            LEFT JOIN estado_turno et ON a.id_estado_turno = et.id
            ORDER BY a.fecha, a.hora
        """
        rows = self.db.execute_query(query, fetch=True)

        if not rows:
            return []

        return [
            {
                "id_turno": row["id"],
                "fecha": row["fecha"],
                "hora_turno": row["hora"],
                "dni_paciente": row.get("dni_paciente") or "",
                "paciente": f"{row.get('nombre_paciente') or ''} {row.get('apellido_paciente') or ''}".strip(),
                "medico": f"{row.get('nombre_medico') or ''} {row.get('apellido_medico') or ''}".strip(),
                "estado": row.get("estado") or ""
            }
            for row in rows
        ]
    
    def get_slots_by_filters(self, id_especialidad, id_medico, fecha):
            """
            Obtiene slots (disponibles y ocupados) filtrados por especialidad, 
            médico (opcional) y fecha.
            """
            # ⚠️ IMPORTANTE: Esta consulta une 4 tablas para asegurar que el slot
            # esté relacionado con la ESPECIALIDAD Y el MEDICO seleccionados.
            query = """
                SELECT 
                    at.id, at.fecha, at.hora, at.id_paciente, at.id_estado_turno, 
                    at.id_horario_medico,
                    m.nombre as medico_nombre, m.apellido as medico_apellido, m.id as medico_id
                FROM agenda_turno at
                JOIN horario_medico hm ON at.id_horario_medico = hm.id
                JOIN medico m ON hm.id_medico = m.id
                JOIN medico_x_especialidad mxe ON m.id = mxe.id_medico
                WHERE mxe.id_especialidad = ?
                AND at.fecha = ?
            """
            params = [id_especialidad, fecha]
            
            if id_medico is not None:
                query += " AND m.id = ?"
                params.append(id_medico)

            rows = self.db.execute_query(query, params, fetch=True)
            return rows

    def existe_turno(self, fecha, hora, id_medico, dia_semana):
        """
        Verifica si ya existe un turno con:
        - médico
        - fecha real (YYYY-MM-DD)
        - hora
        - día de la semana del horario
        """

        query = """
            SELECT a.id
            FROM agenda_turno a
            JOIN horario_medico h ON a.id_horario_medico = h.id
            WHERE h.id_medico = ?
              AND a.fecha = ?
              AND a.hora = ?
              AND h.dia_semana = ?
        """

        rows = self.db.execute_query(
            query,
            (
                id_medico,
                fecha,
                hora,
                dia_semana
            ),
            fetch=True
        )

        return len(rows) > 0




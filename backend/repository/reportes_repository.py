# backend/repository/reportes_repository.py
from backend.data_base.connection import DataBaseConnection

class ReportesRepository:
    def __init__(self):
        self.db = DataBaseConnection()

    # 1️⃣ Turnos por médico (con paciente, especialidad y estado)
    def get_turnos_por_medico(self, id_medico, fecha_inicio, fecha_fin):
        query = """
            SELECT 
                a.fecha,
                a.hora,
                p.nombre AS nombre_paciente,
                p.apellido AS apellido_paciente,
                e.nombre AS especialidad,
                et.nombre AS estado
            FROM agenda_turno a
            JOIN paciente p ON a.id_paciente = p.id
            JOIN estado_turno et ON a.id_estado_turno = et.id
            JOIN horario_medico hm ON a.id_horario_medico = hm.id
            JOIN medico m ON hm.id_medico = m.id
            JOIN medico_x_especialidad me ON m.id = me.id_medico
            JOIN especialidad e ON me.id_especialidad = e.id
            WHERE m.id = ?
              AND a.fecha BETWEEN ? AND ?
            ORDER BY a.fecha, a.hora
        """
        params = (id_medico, fecha_inicio, fecha_fin)
        rows = self.db.execute_query(query, params, fetch=True)

        if not rows:
            return []

        return [
            {
                "fecha": row["fecha"],
                "hora": row["hora"],
                "paciente": f"{row['nombre_paciente']} {row['apellido_paciente']}",
                "especialidad": row["especialidad"],
                "estado": row["estado"]
            }
            for row in rows
        ]

    # 2️⃣ Cantidad de turnos por especialidad (con porcentaje)
    def get_cantidad_turnos_por_especialidad(self):
        # total de turnos
        total_query = """
            SELECT COUNT(*) AS total
            FROM agenda_turno a
        """
        total_data = self.db.execute_query(total_query, fetch=True)
        total_turnos = total_data[0]["total"] if total_data else 0

        query = """
            SELECT 
                e.nombre AS especialidad,
                COUNT(*) AS cantidad
            FROM agenda_turno a
            JOIN horario_medico hm ON a.id_horario_medico = hm.id
            JOIN medico m ON hm.id_medico = m.id
            JOIN medico_x_especialidad me ON m.id = me.id_medico
            JOIN especialidad e ON me.id_especialidad = e.id
            GROUP BY e.nombre
            ORDER BY cantidad DESC
        """
        data = self.db.execute_query(query, fetch=True)

        if not data:
            return []

        return [
            {
                "especialidad": row["especialidad"],
                "cantidad": row["cantidad"],
                "porcentaje": round((row["cantidad"] / total_turnos * 100), 2) if total_turnos > 0 else 0
            }
            for row in data
        ]

    # 3️⃣ Pacientes atendidos (con médico, especialidad, fecha y dni)
    def get_pacientes_atendidos(self, fecha_inicio, fecha_fin):
        query = """
            SELECT 
                p.nombre AS nombre_paciente,
                p.apellido AS apellido_paciente,
                p.dni,
                a.fecha,
                m.nombre AS nombre_medico,
                m.apellido AS apellido_medico,
                e.nombre AS especialidad
            FROM agenda_turno a
            JOIN paciente p ON a.id_paciente = p.id
            JOIN estado_turno et ON a.id_estado_turno = et.id
            JOIN horario_medico hm ON a.id_horario_medico = hm.id
            JOIN medico m ON hm.id_medico = m.id
            JOIN medico_x_especialidad me ON m.id = me.id_medico
            JOIN especialidad e ON me.id_especialidad = e.id
            WHERE a.fecha BETWEEN ? AND ?
              AND et.nombre = 'Atendido'
            ORDER BY a.fecha
        """
        rows = self.db.execute_query(query, (fecha_inicio, fecha_fin), fetch=True)

        if not rows:
            return []

        return [
            {
                "paciente": f"{row['nombre_paciente']} {row['apellido_paciente']}",
                "dni": row["dni"],
                "fecha_atencion": row["fecha"],
                "medico": f"{row['nombre_medico']} {row['apellido_medico']}",
                "especialidad": row["especialidad"]
            }
            for row in rows
        ]

    # 4️⃣ Asistencia vs Inasistencia
    def get_asistencia_vs_inasistencia(self):
        query = """
            SELECT 
                et.nombre AS estado,
                COUNT(*) AS cantidad
            FROM agenda_turno a
            JOIN estado_turno et ON a.id_estado_turno = et.id
            GROUP BY et.nombre
        """
        data = self.db.execute_query(query, fetch=True)

        asistencias = 0
        inasistencias = 0

        if data:
            for row in data:
                if row["estado"].lower() == "atendido":
                    asistencias += row["cantidad"]
                elif row["estado"].lower() in ("ausente", "no asistió", "no asistio"):
                    inasistencias += row["cantidad"]

        return {
            "asistencias": asistencias,
            "inasistencias": inasistencias
        }


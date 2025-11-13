from backend.data_base.connection import DataBaseConnection

class ReportesRepository:
    def __init__(self):
        self.db = DataBaseConnection()

    def get_turnos_por_medico(self, id_medico: int, fecha_inicio: str, fecha_fin: str):
        query = """
            SELECT 
                t.id AS id_turno,
                t.fecha,
                t.hora,
                p.nombre AS paciente,
                e.nombre AS especialidad
            FROM turno t
            JOIN medico m ON t.id_medico = m.id
            JOIN paciente p ON t.id_paciente = p.id
            JOIN especialidad e ON m.id_especialidad = e.id
            WHERE t.id_medico = %s AND t.fecha BETWEEN %s AND %s
            ORDER BY t.fecha, t.hora
        """
        params = (id_medico, fecha_inicio, fecha_fin)
        return self.db.execute_query(query, params, fetch=True)

    def get_cantidad_turnos_por_especialidad(self, fecha_inicio: str, fecha_fin: str):
        query = """
            SELECT 
                e.nombre AS especialidad,
                COUNT(t.id) AS cantidad_turnos
            FROM turno t
            JOIN medico m ON t.id_medico = m.id
            JOIN especialidad e ON m.id_especialidad = e.id
            WHERE t.fecha BETWEEN %s AND %s
            GROUP BY e.nombre
            ORDER BY cantidad_turnos DESC
        """
        params = (fecha_inicio, fecha_fin)
        return self.db.execute_query(query, params, fetch=True)

    def get_pacientes_atendidos(self, fecha_inicio: str, fecha_fin: str):
        query = """
            SELECT DISTINCT 
                p.id, p.nombre, p.apellido, p.dni
            FROM visita v
            JOIN agenda_turno a ON v.id_turno = a.id
            JOIN paciente p ON a.id_paciente = p.id
            WHERE a.fecha BETWEEN %s AND %s
            ORDER BY p.apellido, p.nombre
        """
        params = (fecha_inicio, fecha_fin)
        return self.db.execute_query(query, params, fetch=True)

    def get_asistencia_vs_inasistencia(self, fecha_inicio: str, fecha_fin: str):
        query = """
            SELECT 
                SUM(CASE WHEN t.asistio = 1 THEN 1 ELSE 0 END) AS asistencias,
                SUM(CASE WHEN t.asistio = 0 THEN 1 ELSE 0 END) AS inasistencias
            FROM turno t
            WHERE t.fecha BETWEEN %s AND %s
        """
        params = (fecha_inicio, fecha_fin)
        result = self.db.execute_query(query, params, fetch=True)
        return result[0] if result else {"asistencias": 0, "inasistencias": 0}

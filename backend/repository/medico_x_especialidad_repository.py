from backend.data_base.connection import DataBaseConnection

class MedicoXEspecialidadRepository:
    def __init__(self):
        self.db = DataBaseConnection()

    def add(self, id_medico: int, id_especialidad: int):
        query = "INSERT INTO medico_x_especialidad (id_medico, id_especialidad) VALUES (?, ?)"
        return self.db.execute_query(query, (id_medico, id_especialidad))

    def remove_all_for_medico(self, id_medico: int):
        query = "DELETE FROM medico_x_especialidad WHERE id_medico = ?"
        return self.db.execute_query(query, (id_medico,))

    def list_especialidad_ids_for_medico(self, id_medico: int):
        query = "SELECT id_especialidad FROM medico_x_especialidad WHERE id_medico = ?"
        rows = self.db.execute_query(query, (id_medico,), fetch=True)
        return [r["id_especialidad"] for r in rows] if rows else []

    # ✅ NUEVO: buscar médicos por nombre de especialidad
    def list_medicos_by_especialidad_nombre(self, nombre_especialidad: str):
        query = """
            SELECT m.id, m.nombre, m.apellido, m.matricula
            FROM medico m
            JOIN medico_x_especialidad me ON m.id = me.id_medico
            JOIN especialidad e ON e.id = me.id_especialidad
            WHERE LOWER(e.nombre) = LOWER(?)
        """
        rows = self.db.execute_query(query, (nombre_especialidad,), fetch=True)

        return rows or []

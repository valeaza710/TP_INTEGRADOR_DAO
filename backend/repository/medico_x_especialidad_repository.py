from backend.data_base.connection import DataBaseConnection

class MedicoXEspecialidadRepository:
    def __init__(self):
        self.db = DataBaseConnection()

    def add(self, id_medico: int, id_especialidad: int):
        query = "INSERT INTO medico_x_especialidad (id_medico, id_especialidad) VALUES (%s, %s)"
        return self.db.execute_query(query, (id_medico, id_especialidad))

    def remove_all_for_medico(self, id_medico: int):
        query = "DELETE FROM medico_x_especialidad WHERE id_medico = %s"
        return self.db.execute_query(query, (id_medico,))

    def list_especialidad_ids_for_medico(self, id_medico: int):
        query = "SELECT id_especialidad FROM medico_x_especialidad WHERE id_medico = %s"
        rows = self.db.execute_query(query, (id_medico,), fetch=True)
        return [r['id_especialidad'] for r in rows] if rows else []

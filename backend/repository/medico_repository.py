from data_base.connection import DataBaseConnection

class MedicoRepository:
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, medico):
        query = """INSERT INTO medico (nombre, apellido, matricula, id_usuario)
                   VALUES (%s,%s,%s,%s)"""
        params = (medico.nombre, medico.apellido, medico.matricula, medico.id_usuario)
        return self.db.execute_query(query, params)

    def get_all(self):
        return self.db.execute_query("SELECT * FROM medico", fetch=True)

    def get_by_id(self, medico_id):
        return self.db.execute_query("SELECT * FROM medico WHERE id = %s", (medico_id,), fetch=True)

    def delete(self, medico_id):
        return self.db.execute_query("DELETE FROM medico WHERE id = %s", (medico_id,))

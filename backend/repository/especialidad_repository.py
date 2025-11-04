from data_base.connection import DataBaseConnection

class EspecialidadRepository:
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, especialidad):
        query = "INSERT INTO especialidad (nombre) VALUES (%s)"
        return self.db.execute_query(query, (especialidad.nombre,))

    def get_all(self):
        return self.db.execute_query("SELECT * FROM especialidad", fetch=True)

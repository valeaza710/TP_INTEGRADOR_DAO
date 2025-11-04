from data_base.connection import DataBaseConnection

class PacienteRepository:
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, paciente):
        query = """
        INSERT INTO paciente (nombre, apellido, dni, edad, fecha_nacimiento, mail, telefono, direccion, id_usuario)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (
            paciente.nombre,
            paciente.apellido,
            paciente.dni,
            paciente.edad,
            paciente.fecha_nacimiento,
            paciente.mail,
            paciente.telefono,
            paciente.direccion,
            paciente.id_usuario
        )
        return self.db.execute_query(query, params)

    def get_all(self):
        return self.db.execute_query("SELECT * FROM paciente", fetch=True)

    def get_by_id(self, paciente_id):
        return self.db.execute_query("SELECT * FROM paciente WHERE id = %s", (paciente_id,), fetch=True)

    def delete(self, paciente_id):
        return self.db.execute_query("DELETE FROM paciente WHERE id = %s", (paciente_id,))

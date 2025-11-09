from backend.data_base.connection import DataBaseConnection
from backend.clases.especialidad import Especialidad
from backend.repository.repository import Repository

class EspecialidadRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, especialidad: Especialidad):
        query = """
            INSERT INTO especialidad (nombre)
            VALUES (%s)
        """
        params = (especialidad.nombre,)

        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            especialidad.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return especialidad
        except Exception as e:
            print(f"❌ Error al guardar especialidad: {e}")
            return None


    def get_by_id(self, especialidad_id: int):
        query = "SELECT * FROM especialidad WHERE id = %s"
        data = self.db.execute_query(query, (especialidad_id,), fetch=True)
        if not data:
            return None
        row = data[0]
        return Especialidad(id=row["id"], nombre=row["nombre"])

    def get_all(self):
        query = "SELECT * FROM especialidad"
        especialidades_data = self.db.execute_query(query, fetch=True)
        especialidades = []

        if especialidades_data:
            for row in especialidades_data:
                especialidad = Especialidad(
                    id=row["id"],
                    nombre=row["nombre"]
                )
                especialidades.append(especialidad)
        return especialidades

    def modify(self, especialidad: Especialidad):
        query = """
            UPDATE especialidad 
            SET nombre=%s
            WHERE id=%s
        """
        params = (especialidad.nombre, especialidad.id)
        success = self.db.execute_query(query, params)
        return especialidad if success else None


    def delete(self, especialidad: Especialidad):
        query = "DELETE FROM especialidad WHERE id = %s"
        success = self.db.execute_query(query, (especialidad.id,))
        return success

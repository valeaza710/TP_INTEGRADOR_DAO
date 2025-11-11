from backend.data_base.connection import DataBaseConnection
from backend.clases.especialidad import Especialidad
from backend.repository.repository import Repository


class EspecialidadRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, especialidad: Especialidad):
        query = """
            INSERT INTO especialidad (nombre)
            VALUES (?)
        """
        params = (especialidad.nombre,)

        conn = None
        cursor = None

        try:
            conn = self.db.connect()
            if not conn:
                print("❌ Error al conectar con la base de datos.")
                return None

            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            especialidad.id = cursor.lastrowid
            return especialidad

        except Exception as e:
            print(f"❌ Error al guardar especialidad: {e}")
            if conn:
                conn.rollback()
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_id(self, especialidad_id: int):
        query = "SELECT * FROM especialidad WHERE id = ?"
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
            SET nombre = ?
            WHERE id = ?
        """
        params = (especialidad.nombre, especialidad.id)
        success = self.db.execute_query(query, params)
        return especialidad if success else None

    def delete(self, especialidad: Especialidad):
        query = "DELETE FROM especialidad WHERE id = ?"
        success = self.db.execute_query(query, (especialidad.id,))
        return success

    def exists_by_nombre(self, nombre: str) -> bool:
        query = "SELECT COUNT(*) as count FROM especialidad WHERE nombre = ?"
        result = self.db.execute_query(query, (nombre,), fetch=True)
        return result[0]['count'] > 0 if result else False

    def get_by_nombre(self, nombre: str):
        query = "SELECT * FROM especialidad WHERE nombre = ?"
        data = self.db.execute_query(query, (nombre,), fetch=True)
        if not data:
            return None
        row = data[0]
        return Especialidad(id=row["id"], nombre=row["nombre"])

    def tiene_medicos_asociados(self, especialidad_id: int) -> bool:
        query = "SELECT COUNT(*) as count FROM medico WHERE especialidad_id = ?"
        result = self.db.execute_query(query, (especialidad_id,), fetch=True)
        return result[0]['count'] > 0 if result else False

    def search_by_nombre(self, nombre_parcial: str):
        query = "SELECT * FROM especialidad WHERE nombre LIKE ?"
        especialidades_data = self.db.execute_query(query, (f"%{nombre_parcial}%",), fetch=True)
        especialidades = []
        if especialidades_data:
            for row in especialidades_data:
                especialidad = Especialidad(id=row["id"], nombre=row["nombre"])
                especialidades.append(especialidad)
        return especialidades

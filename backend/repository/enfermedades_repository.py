from backend.data_base.connection import DataBaseConnection
from backend.clases.enfermedad import Enfermedad
from backend.repository.repository import Repository


class EnfermedadRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, enfermedad: Enfermedad):
        query = "INSERT INTO enfermedad (nombre, descripcion) VALUES (?, ?)"
        params = (enfermedad.nombre, enfermedad.descripcion)

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
            enfermedad.id = cursor.lastrowid
            return enfermedad

        except Exception as e:
            print(f"❌ Error al guardar enfermedad: {e}")
            return None

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def get_by_id(self, enfermedad_id: int):
        query = "SELECT * FROM enfermedades WHERE id = ?"
        data = self.db.execute_query(query, (enfermedad_id,), fetch=True)
        if not data:
            return None
        row = data[0]
        return Enfermedad(
            id=row["id"],
            nombre=row["nombre"],
            descripcion=row["descripcion"]
        )

    def get_all(self):
        query = "SELECT * FROM enfermedades"
        rows = self.db.execute_query(query, fetch=True)
        enfermedades = []
        if rows:
            for row in rows:
                enfermedades.append(
                    Enfermedad(
                        id=row["id"],
                        nombre=row["nombre"],
                        descripcion=row["descripcion"]
                    )
                )
        return enfermedades

    def modify(self, enfermedad: Enfermedad):
        query = "UPDATE enfermedades SET nombre = ?, descripcion = ? WHERE id = ?"
        params = (enfermedad.nombre, enfermedad.descripcion, enfermedad.id)
        success = self.db.execute_query(query, params)
        return self.get_by_id(enfermedad.id) if success else None

    def delete(self, enfermedad: Enfermedad):
        query = "DELETE FROM enfermedades WHERE id = ?"
        success = self.db.execute_query(query, (enfermedad.id,))
        return success

    def search_by_nombre(self, nombre_parcial: str):
        query = "SELECT * FROM enfermedades WHERE nombre LIKE ?"
        rows = self.db.execute_query(query, (f'%{nombre_parcial}%',), fetch=True)
        enfermedades = []
        if rows:
            for row in rows:
                enfermedades.append(
                    Enfermedad(
                        id=row["id"],
                        nombre=row["nombre"],
                        descripcion=row["descripcion"]
                    )
                )
        return enfermedades
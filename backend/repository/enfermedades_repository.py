from data_base.connection import DataBaseConnection
from clases.enfermedad import Enfermedad

class EnfermedadRepository:
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, enfermedad: Enfermedad):
        query = "INSERT INTO enfermedad (nombre, descripcion) VALUES (%s, %s)"
        params = (enfermedad.nombre, enfermedad.descripcion)

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            enfermedad.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return enfermedad
        except Exception as e:
            print(f"❌ Error al guardar enfermedad: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_by_id(self, enfermedad_id: int):
        query = "SELECT * FROM enfermedad WHERE id = %s"
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
        query = "SELECT * FROM enfermedad"
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
        query = "UPDATE enfermedad SET nombre=%s, descripcion=%s WHERE id=%s"
        params = (enfermedad.nombre, enfermedad.descripcion, enfermedad.id)
        success = self.db.execute_query(query, params)
        return self.get_by_id(enfermedad.id) if success else None

    def delete(self, enfermedad: Enfermedad):
        query = "DELETE FROM enfermedad WHERE id=%s"
        success = self.db.execute_query(query, (enfermedad.id,))
        return success

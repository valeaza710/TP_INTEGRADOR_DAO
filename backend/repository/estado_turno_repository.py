from backend.data_base.connection import DataBaseConnection
from backend.clases.estado_turno import EstadoTurno
from backend.repository.repository import Repository

class EstadoTurnoRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, estado: EstadoTurno):
        query = "INSERT INTO estado_turno (nombre) VALUES (%s)"
        params = (estado.nombre,)

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            estado.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return estado
        except Exception as e:
            print(f"❌ Error al guardar estado_turno: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_by_id(self, estado_id: int):
        query = "SELECT * FROM estado_turno WHERE id = %s"
        rows = self.db.execute_query(query, (estado_id,), fetch=True)
        if not rows:
            return None
        row = rows[0]
        return EstadoTurno(id=row["id"], nombre=row["nombre"])

    def get_all(self):
        query = "SELECT * FROM estado_turno ORDER BY id"
        rows = self.db.execute_query(query, fetch=True)
        estados = []
        if rows:
            for row in rows:
                estados.append(EstadoTurno(id=row["id"], nombre=row["nombre"]))
        return estados

    def modify(self, estado: EstadoTurno):
        query = "UPDATE estado_turno SET nombre = %s WHERE id = %s"
        params = (estado.nombre, estado.id)
        success = self.db.execute_query(query, params)
        return self.get_by_id(estado.id) if success else None

    def delete(self, estado: EstadoTurno):
        query = "DELETE FROM estado_turno WHERE id = %s"
        success = self.db.execute_query(query, (estado.id,))
        return success

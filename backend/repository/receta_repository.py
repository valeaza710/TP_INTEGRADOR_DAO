from backend.data_base.connection import DataBaseConnection
from backend.clases.receta import Receta
from backend.repository.repository import Repository
from backend.repository.visita_repository import VisitaRepository
from backend.repository.paciente_repository import PacienteRepository

class RecetaRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()
        self.visita_repo = VisitaRepository()
        self.paciente_repo = PacienteRepository()

    def save(self, receta: Receta):
        query = """
            INSERT INTO receta (id_visita, id_paciente, descripcion, fecha_emision)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            receta.visita.id if receta.visita else None,
            receta.paciente.id if receta.paciente else None,
            receta.descripcion,
            receta.fecha_emision
        )

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            receta.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return receta
        except Exception as e:
            print(f"❌ Error al guardar receta: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_by_id(self, receta_id: int):
        query = "SELECT * FROM receta WHERE id = %s"
        rows = self.db.execute_query(query, (receta_id,), fetch=True)
        if not rows:
            return None
        row = rows[0]

        visita = self.visita_repo.get_by_id(row["id_visita"]) if row.get("id_visita") else None
        paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row.get("id_paciente") else None

        return Receta(
            id=row["id"],
            visita=visita,
            paciente=paciente,
            descripcion=row.get("descripcion", ""),
            fecha_emision=row.get("fecha_emision")
        )

    def get_all(self):
        query = "SELECT * FROM receta"
        rows = self.db.execute_query(query, fetch=True)
        recetas = []
        if rows:
            for row in rows:
                visita = self.visita_repo.get_by_id(row["id_visita"]) if row.get("id_visita") else None
                paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row.get("id_paciente") else None

                recetas.append(Receta(
                    id=row["id"],
                    visita=visita,
                    paciente=paciente,
                    descripcion=row.get("descripcion", ""),
                    fecha_emision=row.get("fecha_emision")
                ))
        return recetas

    def modify(self, receta: Receta):
        query = """
            UPDATE receta
            SET id_visita=%s, id_paciente=%s, descripcion=%s, fecha_emision=%s
            WHERE id=%s
        """
        params = (
            receta.visita.id if receta.visita else None,
            receta.paciente.id if receta.paciente else None,
            receta.descripcion,
            receta.fecha_emision,
            receta.id
        )

        success = self.db.execute_query(query, params)
        return self.get_by_id(receta.id) if success else None

    def delete(self, receta: Receta):
        query = "DELETE FROM receta WHERE id = %s"
        success = self.db.execute_query(query, (receta.id,))
        return success

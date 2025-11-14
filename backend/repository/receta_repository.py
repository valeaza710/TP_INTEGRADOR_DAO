from backend.data_base.connection import DataBaseConnection
from backend.clases.receta import Receta
from backend.clases.visita import Visita
from backend.repository.enfermedades_repository import EnfermedadRepository
from backend.repository.repository import Repository
from backend.repository.visita_repository import VisitaRepository
from backend.repository.paciente_repository import PacienteRepository


class RecetaRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()
        self.visita_repo = VisitaRepository()
        self.paciente_repo = PacienteRepository()
        self.enfermedad_repo = EnfermedadRepository()

    def save(self, receta: Receta):
        query = """
            INSERT INTO receta (id_visita, id_paciente, descripcion, fecha_emision, id_enfermedad)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            receta.visita.id if receta.visita else None,
            receta.paciente.id if receta.paciente else None,
            receta.descripcion,
            receta.fecha_emision,
            receta.enfermedad.id if receta.enfermedad else None
        )

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            receta.id = cursor.lastrowid
            return receta
        except Exception as e:
            print(f"❌ Error al guardar receta: {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def get_by_id(self, receta_id: int):
        query = "SELECT * FROM receta WHERE id = ?"
        rows = self.db.execute_query(query, (receta_id,), fetch=True)
        if not rows:
            return None
        row = rows[0]

        visita = self.visita_repo.get_by_id(row["id_visita"]) if row["id_visita"] else None
        paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row["id_paciente"] else None
        enfermedad = self.enfermedad_repo.get_by_id(row["id_enfermedad"]) if row["id_enfermedad"] else None

        return Receta(
            id=row["id"],
            visita=visita,
            paciente=paciente,
            descripcion=row["descripcion"] if row["descripcion"] else "",
            fecha_emision=row["fecha_emision"],
            enfermedad=enfermedad

        )

    def get_all(self):
        query = "SELECT * FROM receta"
        rows = self.db.execute_query(query, fetch=True)
        recetas = []
        if rows:
            for row in rows:
                visita = self.visita_repo.get_by_id(row["id_visita"]) if row["id_visita"] else None
                paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row["id_paciente"] else None
                enfermedad = self.enfermedad_repo.get_by_id(row["id_enfermedad"]) if row["id_enfermedad"] else None

                recetas.append(Receta(
                    id=row["id"],
                    visita=visita,
                    paciente=paciente,
                    descripcion=row["descripcion"] if row["descripcion"] else "",
                    fecha_emision=row["fecha_emision"],
                    enfermedad=enfermedad
                ))
        return recetas

    def modify(self, receta: Receta):
        query = """
            UPDATE receta
            SET id_visita = ?, id_paciente = ?, descripcion = ?, fecha_emision = ?, id_enfermedad = ?
            WHERE id = ?
        """
        params = (
            receta.visita.id if receta.visita else None,
            receta.paciente.id if receta.paciente else None,
            receta.enfermedad.id if receta.enfermedad else None,
            receta.descripcion,
            receta.fecha_emision,
            receta.id
        )

        success = self.db.execute_query(query, params)
        return self.get_by_id(receta.id) if success else None

    def delete(self, receta: Receta):
        query = "DELETE FROM receta WHERE id = ?"
        success = self.db.execute_query(query, (receta.id,))
        return success

    def get_by_paciente(self, id_paciente: int):
        query = "SELECT * FROM receta WHERE id_paciente = ? ORDER BY fecha_emision DESC"
        rows = self.db.execute_query(query, (id_paciente,), fetch=True)
        recetas = []
        if rows:
            for row in rows:
                paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row["id_paciente"] else None
                visita = self.visita_repo.get_by_id(row["id_visita"]) if row["id_visita"] else None
                enfermedad = self.enfermedad_repo.get_by_id(row["id_enfermedad"]) if row["id_enfermedad"] else None

                recetas.append(Receta(
                    id=row["id"],
                    paciente=paciente,
                    visita=visita,
                    enfermedad=enfermedad,
                    descripcion=row["descripcion"] if row["descripcion"] else "",
                    fecha_emision=row["fecha_emision"]
                ))
        return recetas
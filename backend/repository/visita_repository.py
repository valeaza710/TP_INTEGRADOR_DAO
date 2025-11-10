# backend/repository/visita_repository.py
from data_base.connection import DataBaseConnection
from clases.visita import Visita
from repository.historial_clinico_repository import HistorialClinicoRepository
from repository.agenda_turno_repository import AgendaTurnoRepository
from repository.repository import Repository

class VisitaRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()
        self.historial_repo = HistorialClinicoRepository()
        self.agenda_repo = AgendaTurnoRepository()

    def save(self, visita: Visita):
        query = """
            INSERT INTO visita (id_historial_clinico, id_turno, comentario)
            VALUES (%s, %s, %s)
        """
        params = (
            visita.historial_clinico.id if visita.historial_clinico else None,
            visita.agenda_turno.id if visita.agenda_turno else None,
            visita.comentario
        )

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            visita.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return visita
        except Exception as e:
            print(f"❌ Error al guardar visita: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_by_id(self, visita_id: int):
        query = "SELECT * FROM visita WHERE id = %s"
        rows = self.db.execute_query(query, (visita_id,), fetch=True)
        if not rows:
            return None
        row = rows[0]

        historial = self.historial_repo.get_by_id(row["id_historial_clinico"]) if row.get("id_historial_clinico") else None
        agenda = self.agenda_repo.get_by_id(row["id_turno"]) if row.get("id_turno") else None

        return Visita(
            id=row["id"],
            historial_clinico=historial,
            agenda_turno=agenda,
            comentario=row.get("comentario", "")
        )

    def get_all(self):
        query = "SELECT * FROM visita"
        rows = self.db.execute_query(query, fetch=True)
        visitas = []
        if rows:
            for row in rows:
                historial = self.historial_repo.get_by_id(row["id_historial_clinico"]) if row.get("id_historial_clinico") else None
                agenda = self.agenda_repo.get_by_id(row["id_turno"]) if row.get("id_turno") else None

                visitas.append(Visita(
                    id=row["id"],
                    historial_clinico=historial,
                    agenda_turno=agenda,
                    comentario=row.get("comentario", "")
                ))
        return visitas

    def modify(self, visita: Visita):
        query = """
            UPDATE visita
            SET id_historial_clinico=%s, id_turno=%s, comentario=%s
            WHERE id=%s
        """
        params = (
            visita.historial_clinico.id if visita.historial_clinico else None,
            visita.agenda_turno.id if visita.agenda_turno else None,
            visita.comentario,
            visita.id
        )

        success = self.db.execute_query(query, params)
        return self.get_by_id(visita.id) if success else None

    def delete(self, visita: Visita):
        query = "DELETE FROM visita WHERE id = %s"
        success = self.db.execute_query(query, (visita.id,))
        return success

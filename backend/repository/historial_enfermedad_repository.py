from backend.data_base.connection import DataBaseConnection
from backend.clases.historial_enfermedad import HistorialEnfermedad
from backend.clases.historial_clinico import HistorialClinico
from backend.clases.enfermedad import Enfermedad


class HistorialEnfermedadRepository:
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, historial_enfermedad: HistorialEnfermedad):
        query = """
            INSERT INTO historial_enfermedad (id_historial_clinico, id_enfermedad, fecha_diagnostico, observaciones)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            historial_enfermedad.historial_clinico.id if historial_enfermedad.historial_clinico else None,
            historial_enfermedad.enfermedad.id if historial_enfermedad.enfermedad else None,
            historial_enfermedad.fecha_diagnostico,
            historial_enfermedad.observaciones,
        )

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            historial_enfermedad.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return historial_enfermedad
        except Exception as e:
            print(f"❌ Error al guardar historial_enfermedad: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_by_id(self, id_historial_enfermedad: int):
        query = "SELECT * FROM historial_enfermedad WHERE id = %s"
        data = self.db.execute_query(query, (id_historial_enfermedad,), fetch=True)
        if not data:
            return None
        row = data[0]

        historial = HistorialClinico(id=row["id_historial_clinico"])
        enfermedad = Enfermedad(id=row["id_enfermedad"])

        return HistorialEnfermedad(
            id=row["id"],
            historial_clinico=historial,
            enfermedad=enfermedad,
            fecha_diagnostico=row["fecha_diagnostico"],
            observaciones=row["observaciones"],
        )

    def get_all(self):
        query = "SELECT * FROM historial_enfermedad"
        rows = self.db.execute_query(query, fetch=True)
        historial_enfermedades = []
        if rows:
            for row in rows:
                historial = HistorialClinico(id=row["id_historial_clinico"])
                enfermedad = Enfermedad(id=row["id_enfermedad"])
                historial_enfermedades.append(
                    HistorialEnfermedad(
                        id=row["id"],
                        historial_clinico=historial,
                        enfermedad=enfermedad,
                        fecha_diagnostico=row["fecha_diagnostico"],
                        observaciones=row["observaciones"],
                    )
                )
        return historial_enfermedades

    def modify(self, historial_enfermedad: HistorialEnfermedad):
        query = """
            UPDATE historial_enfermedad
            SET id_historial_clinico=%s, id_enfermedad=%s, fecha_diagnostico=%s, observaciones=%s
            WHERE id=%s
        """
        params = (
            historial_enfermedad.historial_clinico.id if historial_enfermedad.historial_clinico else None,
            historial_enfermedad.enfermedad.id if historial_enfermedad.enfermedad else None,
            historial_enfermedad.fecha_diagnostico,
            historial_enfermedad.observaciones,
            historial_enfermedad.id,
        )
        success = self.db.execute_query(query, params)
        return self.get_by_id(historial_enfermedad.id) if success else None

    def delete(self, historial_enfermedad: HistorialEnfermedad):
        query = "DELETE FROM historial_enfermedad WHERE id=%s"
        success = self.db.execute_query(query, (historial_enfermedad.id,))
        return success

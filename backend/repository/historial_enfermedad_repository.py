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
            VALUES (?, ?, ?, ?)
        """
        params = (
            historial_enfermedad.historial_clinico.id if historial_enfermedad.historial_clinico else None,
            historial_enfermedad.enfermedad.id if historial_enfermedad.enfermedad else None,
            historial_enfermedad.fecha_diagnostico,
            historial_enfermedad.observaciones,
        )

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
            historial_enfermedad.id = cursor.lastrowid
            return historial_enfermedad

        except Exception as e:
            print(f"❌ Error al guardar historial_enfermedad: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_id(self, id_historial_enfermedad: int):
        query = "SELECT * FROM historial_enfermedad WHERE id = ?"
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

    def get_by_paciente(self, id_paciente: int):
        try:
            query = """
                SELECT he.id AS id,
                       he.fecha_diagnostico,
                       he.observaciones,
                       he.id_historial_clinico,
                       he.id_enfermedad,
                       e.nombre AS enfermedad_nombre
                FROM historial_enfermedad he
                JOIN historial_clinico hc ON he.id_historial_clinico = hc.id
                JOIN enfermedad e ON he.id_enfermedad = e.id
                WHERE hc.id_paciente = ?
            """

            rows = self.db.execute_query(query, (id_paciente,), fetch=True)

            if not rows:
                return []

            historiales = []
            for r in rows:
                historial = HistorialEnfermedad(
                    id=r["id"],
                    historial_clinico=HistorialClinico(id=r["id_historial_clinico"]),
                    enfermedad=Enfermedad(
                        id=r["id_enfermedad"],
                        nombre=r["enfermedad_nombre"]
                    ),
                    fecha_diagnostico=r["fecha_diagnostico"],
                    observaciones=r["observaciones"]
                )
                historiales.append(historial)

            return historiales

        except Exception as e:
            print(f"❌ Error en get_by_paciente: {e}")
            return []

    def modify(self, historial_enfermedad: HistorialEnfermedad):
        query = """
            UPDATE historial_enfermedad
            SET id_historial_clinico=?, id_enfermedad=?, fecha_diagnostico=?, observaciones=?
            WHERE id=?
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
        query = "DELETE FROM historial_enfermedad WHERE id=?"
        success = self.db.execute_query(query, (historial_enfermedad.id,))
        return success

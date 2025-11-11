
from backend.data_base.connection import DataBaseConnection
from backend.clases.historial_clinico import HistorialClinico
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.repository import Repository
from backend.clases.paciente import Paciente

class HistorialClinicoRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()
        self.paciente_repo = PacienteRepository()

    def save(self, historial: HistorialClinico):
        """
        Inserta un registro en historial_clinico.
        Tabla (según tu dump): id, id_paciente, peso, altura, grupo_sanguineo
        """
        query = """
            INSERT INTO historial_clinico (id_paciente, peso, altura, grupo_sanguineo)
            VALUES (%s, %s, %s, %s)
        """
        paciente_id = historial.paciente.id if (historial.paciente and hasattr(historial.paciente, "id")) else None
        params = (paciente_id, historial.peso, historial.altura, historial.grupo_sanguineo)

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            historial.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return historial
        except Exception as e:
            print(f"❌ Error al guardar historial_clinico: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_by_id(self, historial_id: int):
        query = "SELECT * FROM historial_clinico WHERE id = %s"
        rows = self.db.execute_query(query, (historial_id,), fetch=True)
        if not rows:
            return None
        row = rows[0]

        paciente = None
        if row.get("id_paciente"):
            paciente = self.paciente_repo.get_by_id(row["id_paciente"])

        return HistorialClinico(
            id=row["id"],
            paciente=paciente,
            peso=row.get("peso", 0.0),
            altura=row.get("altura", 0.0),
            grupo_sanguineo=row.get("grupo_sanguineo", "")
        )

    def get_all(self):
        query = "SELECT * FROM historial_clinico"
        rows = self.db.execute_query(query, fetch=True)
        resultados = []
        if rows:
            for row in rows:
                paciente = None
                if row.get("id_paciente"):
                    paciente = self.paciente_repo.get_by_id(row["id_paciente"])
                resultados.append(HistorialClinico(
                    id=row["id"],
                    paciente=paciente,
                    peso=row.get("peso", 0.0),
                    altura=row.get("altura", 0.0),
                    grupo_sanguineo=row.get("grupo_sanguineo", "")
                ))
        return resultados

    def modify(self, historial: HistorialClinico):
        """
        Actualiza peso, altura y grupo_sanguineo y la FK id_paciente si se proporciona.
        """
        query = """
            UPDATE historial_clinico
            SET id_paciente=%s, peso=%s, altura=%s, grupo_sanguineo=%s
            WHERE id=%s
        """
        paciente_id = historial.paciente.id if (historial.paciente and hasattr(historial.paciente, "id")) else None
        params = (paciente_id, historial.peso, historial.altura, historial.grupo_sanguineo, historial.id)

        success = self.db.execute_query(query, params)
        return self.get_by_id(historial.id) if success else None

    def delete(self, historial: HistorialClinico):
        query = "DELETE FROM historial_clinico WHERE id = %s"
        success = self.db.execute_query(query, (historial.id,))
        return success

    def get_by_paciente(self, id_paciente: int):
    # """
    #     Devuelve el historial clínico asociado a un paciente.
    # """
        query = "SELECT * FROM historial_clinico WHERE id_paciente = %s"
        rows = self.db.execute_query(query, (id_paciente,), fetch=True)

        if not rows:
            return None

        row = rows[0]
        paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row.get("id_paciente") else None

        return HistorialClinico(
            id=row["id"],
            paciente=paciente,
            peso=row.get("peso", 0.0),
            altura=row.get("altura", 0.0),
            grupo_sanguineo=row.get("grupo_sanguineo", "")
    )
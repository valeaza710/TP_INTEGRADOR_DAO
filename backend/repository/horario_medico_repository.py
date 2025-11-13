from backend.data_base.connection import DataBaseConnection
from backend.clases.horario_medico import HorarioMedico
from backend.clases.medico import Medico
from backend.repository.medico_repository import MedicoRepository
from backend.repository.repository import Repository


class HorarioMedicoRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()
        self.med_repo = MedicoRepository()

    def save(self, horario: HorarioMedico):
        """
        Inserta un HorarioMedico. Espera horario.medico como objeto Medico.
        Si medico.id es None, intenta guardarlo primero via MedicoRepository.
        Devuelve el objeto HorarioMedico con id seteado o None si hubo error.
        """
        if horario.medico is None:
            print("❌ Error al guardar horario: el atributo 'medico' es None")
            return None

        if horario.medico.id is None:
            saved_med = self.med_repo.save(horario.medico)
            if saved_med is None:
                print("❌ Error al guardar horario: no se pudo guardar el médico asociado")
                return None
            horario.medico = saved_med

        query = """
            INSERT INTO horario_medico (id_medico, mes, anio, dia_semana, hora_inicio, hora_fin, duracion_turno_min)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            horario.medico.id,
            horario.mes,
            horario.anio,
            horario.dia_semana,
            horario.hora_inicio,
            horario.hora_fin,
            horario.duracion_turno_min
        )

        conn = None
        cursor = None
        try:
            conn = self.db.connect()
            if not conn:
                print("❌ Error al guardar horario: no hay conexión a la BD")
                return None

            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            horario.id = cursor.lastrowid
            return horario
        except Exception as e:
            print(f"❌ Error al guardar horario médico: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_id(self, horario_id: int):
        print(f"🔹 horario_repo.get_by_id - horario_id={horario_id}")
        query = "SELECT * FROM horario_medico WHERE id = ?"
        
        try:
            rows = self.db.execute_query(query, (horario_id,), fetch=True)
            print(f"   🔹 Filas obtenidas: {len(rows)}")
        except Exception as e:
            print(f"   ❌ Error ejecutando query: {e}")
            raise

        if not rows:
            print("   ℹ️ No se encontró el horario")
            return None

        row = rows[0]
        print(f"   🔹 Procesando row: {row}")

        medico = None
        if row.get("id_medico"):
            try:
                print(f"      🔹 Obteniendo médico ID={row['id_medico']}")
                medico = self.med_repo.get_by_id(row["id_medico"])
                print(f"      ✅ Médico obtenido: {medico}")
            except Exception as e:
                print(f"      ❌ Error obteniendo médico: {e}")
                raise

        try:
            horario = HorarioMedico(
                id=row["id"],
                medico=medico,
                mes=row.get("mes"),
                anio=row.get("anio"),
                dia_semana=row.get("dia_semana"),
                hora_inicio=row.get("hora_inicio"),
                hora_fin=row.get("hora_fin"),
                duracion_turno_min=row.get("duracion_turno_min")
            )
            print(f"   ✅ Horario mapeado: {horario}")
            return horario
        except Exception as e:
            print(f"   ❌ Error construyendo HorarioMedico: {e}")
            raise


    def get_by_medico(self, medico: Medico):
        """
        Devuelve la lista de HorarioMedico para un objeto Medico (puede pasarse Medico o un Medico con solo id).
        """
        if medico is None or medico.id is None:
            return []

        query = "SELECT * FROM horario_medico WHERE id_medico = ? ORDER BY anio, mes, dia_semana, hora_inicio"
        rows = self.db.execute_query(query, (medico.id,), fetch=True)
        horarios = []

        if rows:
            for r in rows:
                med_obj = self.med_repo.get_by_id(r["id_medico"]) or medico
                horarios.append(HorarioMedico(
                    id=r["id"],
                    medico=med_obj,
                    mes=r.get("mes"),
                    anio=r.get("anio"),
                    dia_semana=r.get("dia_semana"),
                    hora_inicio=r.get("hora_inicio"),
                    hora_fin=r.get("hora_fin"),
                    duracion_turno_min=r.get("duracion_turno_min")
                ))
        return horarios

    def get_all(self):
        query = "SELECT * FROM horario_medico"
        rows = self.db.execute_query(query, fetch=True)
        horarios = []
        if not rows:
            return horarios

        medico_ids = sorted({r["id_medico"] for r in rows if r.get("id_medico")})
        med_by_id = {}

        if medico_ids:
            placeholders = ", ".join(["?"] * len(medico_ids))
            q = f"SELECT * FROM medico WHERE id IN ({placeholders})"
            med_rows = self.db.execute_query(q, tuple(medico_ids), fetch=True) or []
            for mr in med_rows:
                med_by_id[mr["id"]] = self.med_repo.get_by_id(mr["id"])

        for r in rows:
            med_obj = med_by_id.get(r.get("id_medico"))
            horarios.append(HorarioMedico(
                id=r["id"],
                medico=med_obj,
                mes=r.get("mes"),
                anio=r.get("anio"),
                dia_semana=r.get("dia_semana"),
                hora_inicio=r.get("hora_inicio"),
                hora_fin=r.get("hora_fin"),
                duracion_turno_min=r.get("duracion_turno_min")
            ))
        return horarios

    def modify(self, horario: HorarioMedico):
        if horario.medico is None:
            print("❌ Error al modificar horario: 'medico' es None")
            return None

        if horario.medico.id is None:
            saved_med = self.med_repo.save(horario.medico)
            if saved_med is None:
                print("❌ Error al modificar horario: no se pudo guardar el médico asociado")
                return None
            horario.medico = saved_med

        query = """
            UPDATE horario_medico
            SET id_medico=?, mes=?, anio=?, dia_semana=?, hora_inicio=?, hora_fin=?, duracion_turno_min=?
            WHERE id=?
        """
        params = (
            horario.medico.id,
            horario.mes,
            horario.anio,
            horario.dia_semana,
            horario.hora_inicio,
            horario.hora_fin,
            horario.duracion_turno_min,
            horario.id
        )
        success = self.db.execute_query(query, params)
        return self.get_by_id(horario.id) if success else None

    def delete(self, horario: HorarioMedico):
        query = "DELETE FROM horario_medico WHERE id = ?"
        success = self.db.execute_query(query, (horario.id,))
        return success

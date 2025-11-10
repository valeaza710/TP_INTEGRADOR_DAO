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
        # Asegurar que exista medico.id
        if horario.medico is None:
            print("❌ Error al guardar horario: el atributo 'medico' es None")
            return None

        if horario.medico.id is None:
            # si el médico no tiene id, lo guardamos primero
            saved_med = self.med_repo.save(horario.medico)
            if saved_med is None:
                print("❌ Error al guardar horario: no se pudo guardar el médico asociado")
                return None
            horario.medico = saved_med

        query = """
            INSERT INTO horario_medico (id_medico, mes, anio, dia_semana, hora_inicio, hora_fin, duracion_turno_min)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
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

        conn = self.db.connect()
        if not conn:
            print("❌ Error al guardar horario: no hay conexión a la BD")
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            horario.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return horario
        except Exception as e:
            print(f"❌ Error al guardar horario médico: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_by_id(self, horario_id: int):
        query = "SELECT * FROM horario_medico WHERE id = %s"
        rows = self.db.execute_query(query, (horario_id,), fetch=True)
        if not rows:
            return None
        row = rows[0]

        # cargar medico asociado
        medico = None
        if row.get("id_medico"):
            medico = self.med_repo.get_by_id(row["id_medico"])

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
        return horario

    def get_by_medico(self, medico: Medico):
        """
        Devuelve la lista de HorarioMedico para un objeto Medico (puede pasarse Medico o un Medico con solo id).
        """
        if medico is None:
            return []

        medico_id = medico.id
        if medico_id is None:
            # si el objeto Medico no tiene id, no hay horarios persistidos
            return []

        query = "SELECT * FROM horario_medico WHERE id_medico = %s ORDER BY anio, mes, dia_semana, hora_inicio"
        rows = self.db.execute_query(query, (medico_id,), fetch=True)
        horarios = []
        if rows:
            for r in rows:
                # reutilizamos med_repo para traer el objeto completo (o podemos usar el mismo 'medico' pasado)
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

        # para eficiencia, cargamos todos los médicos referenciados en batch
        medico_ids = sorted({r['id_medico'] for r in rows if r.get('id_medico')})
        med_by_id = {}
        if medico_ids:
            # consultamos todos los médicos necesarios de una
            q = f"SELECT * FROM medico WHERE id IN ({', '.join(['%s']*len(medico_ids))})"
            med_rows = self.db.execute_query(q, tuple(medico_ids), fetch=True) or []
            for mr in med_rows:
                med_by_id[mr['id']] = self.med_repo.get_by_id(mr['id'])  # reutiliza lógica de MedicoRepository

        for r in rows:
            med_obj = med_by_id.get(r.get('id_medico'))
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
        """
        Actualiza registro. Espera horario.medico como objeto (si tiene id distinto se usa el id).
        """
        if horario.medico is None:
            print("❌ Error al modificar horario: 'medico' es None")
            return None

        if horario.medico.id is None:
            # intentamos persistir el médico si no tiene id
            saved_med = self.med_repo.save(horario.medico)
            if saved_med is None:
                print("❌ Error al modificar horario: no se pudo guardar el médico asociado")
                return None
            horario.medico = saved_med

        query = """
            UPDATE horario_medico
            SET id_medico=%s, mes=%s, anio=%s, dia_semana=%s, hora_inicio=%s, hora_fin=%s, duracion_turno_min=%s
            WHERE id=%s
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
        query = "DELETE FROM horario_medico WHERE id = %s"
        success = self.db.execute_query(query, (horario.id,))
        return success

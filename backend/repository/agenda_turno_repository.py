from backend.data_base.connection import DataBaseConnection
from backend.clases.agenda_turno import AgendaTurno
from backend.repository.paciente_repository import PacienteRepository
from backend.repository.estado_turno_repository import EstadoTurnoRepository
from backend.repository.horario_medico_repository import HorarioMedicoRepository
from backend.repository.repository import Repository
from datetime import date
from backend.data_base.connection import DataBaseConnection

class AgendaTurnoRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()
        self.paciente_repo = PacienteRepository()
        self.estado_repo = EstadoTurnoRepository()
        self.horario_repo = HorarioMedicoRepository()


    def save_many(self, turnos):
        """
        Guarda múltiples objetos AgendaTurno en la base de datos.
        :param turnos: Lista de objetos AgendaTurno.
        :return: Número de filas insertadas.
        """
        query = """
            INSERT INTO agenda_turno (fecha, hora, id_paciente, id_estado_turno, id_horario_medico)
            VALUES (?, ?, ?, ?, ?)
        """

        params = [
            (t.fecha, t.hora, t.id_paciente, t.id_estado_turno, t.id_horario_medico)
            for t in turnos
        ]

        try:
            cur = self.db.cursor()
            cur.executemany(query, params)
            self.db.commit()
            print(f"✅ [DB] {len(params)} turnos guardados masivamente.")
            return len(params)
        except Exception as e:
            # Revertir la transacción en caso de error
            self.db.rollback() 
            print(f"❌ [DB Error] Fallo al guardar turnos masivamente: {e}")
            raise

    
    # -------------------------------------------------------------------------
    # Crear un nuevo turno
    # -------------------------------------------------------------------------
    def save(self, agenda: AgendaTurno):
        query = """
            INSERT INTO agenda_turno (fecha, hora, id_paciente, id_estado_turno, id_horario_medico)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            agenda.fecha,
            agenda.hora,
            agenda.paciente.id if agenda.paciente else None,
            agenda.estado_turno.id if agenda.estado_turno else None,
            agenda.horario_medico.id if agenda.horario_medico else None,
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
            agenda.id = cursor.lastrowid
            return agenda
        except Exception as e:
            print(f"❌ Error al guardar agenda_turno: {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

    # -------------------------------------------------------------------------
    # Obtener un turno por ID
    # -------------------------------------------------------------------------
    def get_by_id(self, agenda_id: int):
        query = "SELECT * FROM agenda_turno WHERE id = ?"
        data = self.db.execute_query(query, (agenda_id,), fetch=True)
        if not data:
            return None
        row = data[0]

        paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row["id_paciente"] else None
        estado = self.estado_repo.get_by_id(row["id_estado_turno"]) if row["id_estado_turno"] else None
        horario = self.horario_repo.get_by_id(row["id_horario_medico"]) if row["id_horario_medico"] else None

        return AgendaTurno(
            id=row["id"],
            fecha=row["fecha"],
            hora=row["hora"],
            paciente=paciente,
            estado_turno=estado,
            horario_medico=horario
        )

    # -------------------------------------------------------------------------
    # Obtener todos los turnos
    # -------------------------------------------------------------------------
    def get_all(self):
        query = "SELECT * FROM agenda_turno"
        data = self.db.execute_query(query, fetch=True)
        agendas = []

        if data:
            for row in data:
                paciente = self.paciente_repo.get_by_id(row["id_paciente"]) if row["id_paciente"] else None
                estado = self.estado_repo.get_by_id(row["id_estado_turno"]) if row["id_estado_turno"] else None
                horario = self.horario_repo.get_by_id(row["id_horario_medico"]) if row["id_horario_medico"] else None

                agendas.append(AgendaTurno(
                    id=row["id"],
                    fecha=row["fecha"],
                    hora=row["hora"],
                    paciente=paciente,
                    estado_turno=estado,
                    horario_medico=horario
                ))

        return agendas

    # -------------------------------------------------------------------------
    # Modificar un turno
    # -------------------------------------------------------------------------
    def modify(self, agenda: AgendaTurno):
        query = """
            UPDATE agenda_turno
            SET fecha = ?, hora = ?, id_paciente = ?, id_estado_turno = ?, id_horario_medico = ?
            WHERE id = ?
        """
        params = (
            agenda.fecha,
            agenda.hora,
            agenda.paciente.id if agenda.paciente else None,
            agenda.estado_turno.id if agenda.estado_turno else None,
            agenda.horario_medico.id if agenda.horario_medico else None,
            agenda.id
        )

        success = self.db.execute_query(query, params)
        return agenda if success else None

    # -------------------------------------------------------------------------
    # Eliminar un turno
    # -------------------------------------------------------------------------
    def delete(self, agenda: AgendaTurno):
        query = "DELETE FROM agenda_turno WHERE id = ?"
        success = self.db.execute_query(query, (agenda.id,))
        return success

    # -------------------------------------------------------------------------
    # Obtener todos los turnos de un médico (excepto estados 1, 4, 5)
    # -------------------------------------------------------------------------
    def get_by_medico(self, id_medico: int):
        query = """
            SELECT a.*
            FROM agenda_turno a
            JOIN horario_medico h ON a.id_horario_medico = h.id
            WHERE h.id_medico = ?
              AND a.id_estado_turno NOT IN (1, 4, 5)
            ORDER BY a.fecha, a.hora
        """

        rows = self.db.execute_query(query, (id_medico,), fetch=True)
        if not rows:
            return []

        turnos = []
        for r in rows:
            turno = self._map_row_to_agenda_turno(r)
            turnos.append(turno)
        return turnos

    # -------------------------------------------------------------------------
    # Convertir objeto AgendaTurno a diccionario (para JSON)
    # -------------------------------------------------------------------------
    def _to_dict(self, a: AgendaTurno):
        if not a:
            return None

        return {
            "id": a.id,
            "fecha": str(a.fecha),
            "hora": str(a.hora),
            "paciente": {
                "id": a.paciente.id,
                "nombre": a.paciente.nombre,
                "apellido": a.paciente.apellido,
                "dni": a.paciente.dni
            } if a.paciente else None,
            "estado_turno": {
                "id": a.estado_turno.id,
                "nombre": a.estado_turno.nombre
            } if a.estado_turno else None,
            "horario_medico": {
                "id": a.horario_medico.id,
                "hora_inicio": str(a.horario_medico.hora_inicio),
                "hora_fin": str(a.horario_medico.hora_fin),
                "medico": {
                    "id": a.horario_medico.medico.id,
                    "nombre": a.horario_medico.medico.nombre,
                    "especialidades": [
                        {"id": e.id, "nombre": e.nombre} for e in a.horario_medico.medico.especialidades
                    ] if a.horario_medico.medico.especialidades else [],
                    "usuario": {
                        "id": a.horario_medico.medico.usuario.id,
                        "username": a.horario_medico.medico.usuario.nombre_usuario,
                        "tipo": a.horario_medico.medico.usuario.tipo_usuario
                    } if a.horario_medico.medico.usuario else None
                }
            } if a.horario_medico else None
        }



    # -------------------------------------------------------------------------
    # Ver turnos ya atendidos por médico (historial)
    # -------------------------------------------------------------------------
    def get_atendidos_by_medico(self, id_medico: int):
        """
        Devuelve todos los turnos de un médico que ya fueron atendidos.
        Se asume que el estado 3 = 'Ya atendido' o como sea que se llame.
        """
        query = """
            SELECT a.*
            FROM agenda_turno a
            JOIN horario_medico h ON a.id_horario_medico = h.id
            WHERE h.id_medico = ?
              AND a.id_estado_turno = 3
            ORDER BY a.fecha DESC, a.hora DESC
        """
        rows = self.db.execute_query(query, (id_medico,), fetch=True)
        if not rows:
            return []

        turnos = []
        for r in rows:
            turnos.append(self._map_row_to_agenda_turno(r))
        return turnos

    # -------------------------------------------------------------------------
    # Obtener turnos del día actual para atender por médico
    # -------------------------------------------------------------------------
    def get_turnos_hoy_by_medico(self, id_medico: int):
        """
        Devuelve los turnos del día actual de un médico.
        Excluye los estados que no correspondan (usa solo Confirmado = 2).
        """
        try:
            hoy = date.today().strftime("%Y-%m-%d")
            query = """
                SELECT a.*
                FROM agenda_turno AS a
                INNER JOIN horario_medico AS h ON a.id_horario_medico = h.id
                WHERE h.id_medico = ?
                    AND a.fecha = ?
                    AND a.id_estado_turno IN (2)
                ORDER BY a.hora ASC
            """

            print(f"Ejecutando query para médico ID={id_medico}")
            rows = self.db.execute_query(query, (id_medico, hoy), fetch=True)
            print(f"Turnos encontrados: {len(rows)}")

            if not rows:
                print("ℹNo hay turnos hoy")
                return []

            turnos = []
            for idx, row in enumerate(rows):
                print(f"🔹 Procesando fila {idx}: {row}")

                # debug dentro del mapping
                try:
                    turno = self._map_row_to_agenda_turno(row)
                    print(f"✅ Turno mapeado: {turno}")
                    turnos.append(turno)
                except Exception as e_map:
                    print(f"❌ Error mapeando fila {idx}: {e_map}")
                    raise

            return turnos

        except Exception as e:
            print(f"❌ Error general en get_turnos_hoy_by_medico: {e}")
            raise



     # -------------------------------------------------------------------------
    # Método auxiliar (ya lo usás en get_by_medico)
    # -------------------------------------------------------------------------
    def _map_row_to_agenda_turno(self, row):
        """
        Mapea una fila de la tabla agenda_turno a un objeto AgendaTurno.
        Incluye debug detallado para identificar errores en repositorios.
        """
        print(f"🔹 _map_row_to_agenda_turno - row: {row}")

        # Inicializamos variables
        paciente = None
        estado = None
        horario = None

        # -------------------------------
        # Obtener paciente
        # -------------------------------
        try:
            if row.get("id_paciente"):
                print(f"   🔹 Obteniendo paciente ID={row['id_paciente']}")
                paciente = self.paciente_repo.get_by_id(row["id_paciente"])
                print(f"   ✅ Paciente obtenido: {paciente}")
            else:
                print("   ℹ️ No hay paciente asociado a este turno")
        except Exception as e:
            print(f"   ❌ Error obteniendo paciente (ID={row.get('id_paciente')}): {e}")
            raise

        # -------------------------------
        # Obtener estado del turno
        # -------------------------------
        try:
            if row.get("id_estado_turno"):
                print(f"   🔹 Obteniendo estado turno ID={row['id_estado_turno']}")
                estado = self.estado_repo.get_by_id(row["id_estado_turno"])
                print(f"   ✅ Estado obtenido: {estado}")
            else:
                print("   ℹ️ No hay estado de turno asociado")
        except Exception as e:
            print(f"   ❌ Error obteniendo estado turno (ID={row.get('id_estado_turno')}): {e}")
            raise

        # -------------------------------
        # Obtener horario del médico
        # -------------------------------
        try:
            if row.get("id_horario_medico"):
                print(f"   🔹 Obteniendo horario médico ID={row['id_horario_medico']}")
                horario = self.horario_repo.get_by_id(row["id_horario_medico"])
                print(f"   ✅ Horario obtenido: {horario}")
            else:
                print("   ℹ️ No hay horario médico asociado")
        except Exception as e:
            print(f"   ❌ Error obteniendo horario médico (ID={row.get('id_horario_medico')}): {e}")
            raise

        # -------------------------------
        # Construir el objeto AgendaTurno
        # -------------------------------
        try:
            turno = AgendaTurno(
                id=row["id"],
                fecha=row["fecha"],
                hora=row["hora"],
                paciente=paciente,
                estado_turno=estado,
                horario_medico=horario
            )
            print(f"   ✅ Turno mapeado correctamente: {turno}")
            return turno
        except Exception as e:
            print(f"   ❌ Error construyendo AgendaTurno: {e}")
            raise

    def get_pacientes_by_medico(self, id_medico: int):
        """
        Devuelve todos los pacientes que alguna vez tuvo el médico,
        más la fecha del último turno atendido (a.id_estado_turno = 3).
        """
        query = """
            SELECT 
                p.*,
                (
                    SELECT a2.fecha
                    FROM agenda_turno a2
                    JOIN horario_medico h2 ON a2.id_horario_medico = h2.id
                    WHERE h2.id_medico = ?
                      AND a2.id_paciente = p.id
                      AND a2.id_estado_turno = 3
                    ORDER BY a2.fecha DESC, a2.hora DESC
                    LIMIT 1
                ) AS ultima_fecha_atendido
            FROM agenda_turno a
            JOIN horario_medico h ON a.id_horario_medico = h.id
            JOIN paciente p ON a.id_paciente = p.id
            WHERE h.id_medico = ? AND a.id_estado_turno = 3
            GROUP BY p.id
            ORDER BY p.apellido, p.nombre
        """

        rows = self.db.execute_query(query, (id_medico, id_medico), fetch=True)
        if not rows:
            return []

        pacientes = []
        for r in rows:
            pacientes.append({
                "id": r["id"],
                "nombre": r["nombre"],
                "apellido": r["apellido"],
                "dni": r["dni"],
                "telefono": r.get("telefono"),
                "obra_social": r.get("obra_social"),
                "ultima_fecha_atendido": r["ultima_fecha_atendido"]
            })
        return pacientes

    def existe_turno(self, fecha, hora, id_medico, dia_semana):
        """
        Verifica si ya existe un turno con:
        - médico
        - fecha real (YYYY-MM-DD)
        - hora
        - día de la semana del horario
        """

        query = """
            SELECT a.id
            FROM agenda_turno a
            JOIN horario_medico h ON a.id_horario_medico = h.id
            WHERE h.id_medico = ?
              AND a.fecha = ?
              AND a.hora = ?
              AND h.dia_semana = ?
        """

        rows = self.db.execute_query(
            query,
            (
                id_medico,
                fecha,
                hora,
                dia_semana
            ),
            fetch=True
        )

        return len(rows) > 0

    def get_todos_los_turnos(self):
        query = """
               SELECT 
                   a.id,
                   a.fecha,
                   a.hora,
                   p.dni AS dni_paciente,
                   p.nombre AS nombre_paciente,
                   p.apellido AS apellido_paciente,
                   m.nombre AS nombre_medico,
                   m.apellido AS apellido_medico,
                   et.nombre AS estado
               FROM agenda_turno a
               LEFT JOIN paciente p ON a.id_paciente = p.id
               LEFT JOIN horario_medico hm ON a.id_horario_medico = hm.id
               LEFT JOIN medico m ON hm.id_medico = m.id
               LEFT JOIN estado_turno et ON a.id_estado_turno = et.id
               ORDER BY a.fecha, a.hora
           """
        rows = self.db.execute_query(query, fetch=True)

        if not rows:
            return []

        return [
            {
                "id_turno": row["id"],
                "fecha": row["fecha"],
                "hora_turno": row["hora"],
                "dni_paciente": row.get("dni_paciente") or "",
                "paciente": f"{row.get('nombre_paciente') or ''} {row.get('apellido_paciente') or ''}".strip(),
                "medico": f"{row.get('nombre_medico') or ''} {row.get('apellido_medico') or ''}".strip(),
                "estado": row.get("estado") or ""
            }
            for row in rows
        ]

    def get_slots_by_filters(self, id_especialidad, id_medico, fecha):
        """
        Obtiene slots (disponibles y ocupados) filtrados por especialidad,
        médico (opcional) y fecha.
        """
        # ⚠️ IMPORTANTE: Esta consulta une 4 tablas para asegurar que el slot
        # esté relacionado con la ESPECIALIDAD Y el MEDICO seleccionados.
        query = """
            SELECT 
                at.id, at.fecha, at.hora, at.id_paciente, at.id_estado_turno, 
                at.id_horario_medico,
                m.nombre as medico_nombre, m.apellido as medico_apellido, m.id as medico_id
            FROM agenda_turno at
            JOIN horario_medico hm ON at.id_horario_medico = hm.id
            JOIN medico m ON hm.id_medico = m.id
            JOIN medico_x_especialidad mxe ON m.id = mxe.id_medico
            WHERE mxe.id_especialidad = ?
            AND at.fecha = ?
        """
        params = [id_especialidad, fecha]

        if id_medico is not None:
            query += " AND m.id = ?"
            params.append(id_medico)

        rows = self.db.execute_query(query, params, fetch=True)
        return rows
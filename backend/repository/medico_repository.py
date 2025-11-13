from backend.data_base.connection import DataBaseConnection
from backend.clases.medico import Medico
from backend.clases.especialidad import Especialidad
from backend.clases.usuario import Usuario
from backend.repository.medico_x_especialidad_repository import MedicoXEspecialidadRepository
from backend.repository.repository import Repository

class MedicoRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()
        self.mxesp_repo = MedicoXEspecialidadRepository()

    def save(self, medico: Medico):
        query = """
            INSERT INTO medico (nombre, apellido, dni, matricula, telefono, mail, direccion, id_usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            medico.nombre,
            medico.apellido,
            medico.dni,
            medico.matricula,
            medico.telefono,
            medico.mail,
            medico.direccion,
            medico.usuario.id if medico.usuario else None,
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
            medico.id = cursor.lastrowid
        except Exception as e:
            print(f"❌ Error al guardar médico: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

        # insertar asociaciones many-to-many
        if medico.especialidades:
            for esp in medico.especialidades:
                try:
                    self.mxesp_repo.add(medico.id, esp.id)
                except Exception as e:
                    print(f"❌ Error al agregar especialidad ({esp.id}) al médico ({medico.id}): {e}")

        return medico

    def get_by_id(self, medico_id: int):
        print(f"🔹 med_repo.get_by_id - medico_id={medico_id}")

        # -------------------------------
        # Buscar médico
        # -------------------------------
        try:
            data = self.db.execute_query("SELECT * FROM medico WHERE id = ?", (medico_id,), fetch=True)
            print(f"   🔹 Filas obtenidas: {len(data)}")
        except Exception as e:
            print(f"   ❌ Error ejecutando query medico: {e}")
            raise

        if not data:
            print("   ℹ️ No se encontró el médico")
            return None

        row = data[0]
        print(f"   🔹 Procesando row: {row}")

        # -------------------------------
        # Cargar usuario asociado
        # -------------------------------
        usuario = None
        if row.get("id_usuario"):
            try:
                print(f"      🔹 Obteniendo usuario ID={row['id_usuario']}")
                udata = self.db.execute_query("SELECT * FROM usuario WHERE id = ?", (row["id_usuario"],), fetch=True)
                print(f"      🔹 Filas usuario obtenidas: {len(udata)}")
                if udata:
                    u = udata[0]
                    usuario = Usuario(
                        id=u["id"],
                        nombre_usuario=u["nombre_usuario"],
                        contrasena=u["contrasena"],
                        tipo_usuario=None
                    )
                    print(f"      ✅ Usuario obtenido: {usuario}")
            except Exception as e:
                print(f"      ❌ Error obteniendo usuario: {e}")
                raise
        else:
            print("      ℹ️ No hay usuario asociado")

        # -------------------------------
        # Cargar especialidades
        # -------------------------------
        especialidades = []
        try:
            esp_ids = self.mxesp_repo.list_especialidad_ids_for_medico(row["id"])
            print(f"      🔹 Especialidades IDs: {esp_ids}")
            if esp_ids:
                placeholders = ", ".join(["?"] * len(esp_ids))
                q = f"SELECT * FROM especialidad WHERE id IN ({placeholders})"
                esp_rows = self.db.execute_query(q, tuple(esp_ids), fetch=True)
                for er in esp_rows:
                    especialidades.append(Especialidad(id=er["id"], nombre=er["nombre"]))
                print(f"      ✅ Especialidades obtenidas: {especialidades}")
        except Exception as e:
            print(f"      ❌ Error obteniendo especialidades: {e}")
            raise

        # -------------------------------
        # Construir objeto Medico
        # -------------------------------
        try:
            medico = Medico(
                id=row["id"],
                nombre=row["nombre"],
                apellido=row["apellido"],
                dni=row.get("dni"),
                matricula=row.get("matricula"),
                telefono=row.get("telefono"),
                mail=row.get("mail"),
                direccion=row.get("direccion"),
                especialidades=especialidades,
                usuario=usuario
            )
            print(f"   ✅ Medico mapeado correctamente: {medico}")
            return medico
        except Exception as e:
            print(f"   ❌ Error construyendo objeto Medico: {e}")
            raise


    def get_all(self):
        query = "SELECT * FROM medico"
        medicos_data = self.db.execute_query(query, fetch=True)
        medicos = []
        if not medicos_data:
            return medicos

        medico_ids = [r['id'] for r in medicos_data]

        placeholders = ", ".join(["?"] * len(medico_ids))
        q_assoc = f"SELECT id_medico, id_especialidad FROM medico_x_especialidad WHERE id_medico IN ({placeholders})"
        assoc_rows = self.db.execute_query(q_assoc, tuple(medico_ids), fetch=True) or []
        esp_map = {}
        for a in assoc_rows:
            esp_map.setdefault(a['id_medico'], []).append(a['id_especialidad'])

        all_esp_ids = sorted({eid for ids in esp_map.values() for eid in ids})
        esp_by_id = {}
        if all_esp_ids:
            placeholders = ", ".join(["?"] * len(all_esp_ids))
            q_esp = f"SELECT * FROM especialidad WHERE id IN ({placeholders})"
            esp_rows = self.db.execute_query(q_esp, tuple(all_esp_ids), fetch=True) or []
            for er in esp_rows:
                esp_by_id[er['id']] = Especialidad(id=er['id'], nombre=er['nombre'])

        user_ids = sorted({r['id_usuario'] for r in medicos_data if r.get('id_usuario')})
        users_by_id = {}
        if user_ids:
            placeholders = ", ".join(["?"] * len(user_ids))
            q_u = f"SELECT * FROM usuario WHERE id IN ({placeholders})"
            u_rows = self.db.execute_query(q_u, tuple(user_ids), fetch=True) or []
            for ur in u_rows:
                users_by_id[ur['id']] = Usuario(id=ur['id'], nombre_usuario=ur['nombre_usuario'], contrasena=ur['contrasena'], tipo_usuario=None)

        for row in medicos_data:
            esp_list = [esp_by_id[eid] for eid in esp_map.get(row['id'], []) if eid in esp_by_id]
            usuario = users_by_id.get(row.get('id_usuario'))
            medico = Medico(
                id=row['id'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                dni=row.get('dni'),
                matricula=row.get('matricula'),
                telefono=row.get('telefono'),
                mail=row.get('mail'),
                direccion=row.get('direccion'),
                especialidades=esp_list,
                usuario=usuario
            )
            medicos.append(medico)
        return medicos

    def modify(self, medico: Medico):
        query = """
            UPDATE medico
            SET nombre=?, apellido=?, dni=?, matricula=?, telefono=?, mail=?, direccion=?, id_usuario=?
            WHERE id=?
        """
        params = (
            medico.nombre,
            medico.apellido,
            medico.dni,
            medico.matricula,
            medico.telefono,
            medico.mail,
            medico.direccion,
            medico.usuario.id if medico.usuario else None,
            medico.id,
        )
        success = self.db.execute_query(query, params)
        if not success:
            return None

        try:
            self.mxesp_repo.remove_all_for_medico(medico.id)
            if medico.especialidades:
                for esp in medico.especialidades:
                    self.mxesp_repo.add(medico.id, esp.id)
        except Exception as e:
            print(f"❌ Error al modificar asociaciones de especialidades para medico {medico.id}: {e}")

        return self.get_by_id(medico.id)

    def delete(self, medico: Medico):
        try:
            self.mxesp_repo.remove_all_for_medico(medico.id)
        except Exception as e:
            print(f"❌ Error al borrar asociaciones de medico {medico.id}: {e}")
        return self.db.execute_query("DELETE FROM medico WHERE id = ?", (medico.id,))

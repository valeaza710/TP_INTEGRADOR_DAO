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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            medico.id = cursor.lastrowid
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Error al guardar médico: {e}")
            return None

        # insertar asociaciones many-to-many
        if medico.especialidades:
            for esp in medico.especialidades:
                try:
                    self.mxesp_repo.add(medico.id, esp.id)
                except Exception as e:
                    print(f"❌ Error al agregar especialidad ({esp.id}) al médico ({medico.id}): {e}")
        return medico

    def get_by_id(self, medico_id: int):
        query = "SELECT * FROM medico WHERE id = %s"
        data = self.db.execute_query(query, (medico_id,), fetch=True)
        if not data:
            return None
        row = data[0]

        # cargar usuario si existe
        usuario = None
        if row.get("id_usuario"):
            udata = self.db.execute_query("SELECT * FROM usuario WHERE id = %s", (row["id_usuario"],), fetch=True)
            if udata:
                u = udata[0]
                usuario = Usuario(id=u["id"], nombre_usuario=u["nombre_usuario"], contrasena=u["contrasena"], tipo_usuario=None)

        # cargar especialidades asociadas
        especialidades = []
        esp_ids = self.mxesp_repo.list_especialidad_ids_for_medico(row["id"])
        if esp_ids:
            # traer todas las especialidades en una sola query
            q = f"SELECT * FROM especialidad WHERE id IN ({', '.join(['%s']*len(esp_ids))})"
            esp_rows = self.db.execute_query(q, tuple(esp_ids), fetch=True)
            for er in esp_rows:
                especialidades.append(Especialidad(id=er["id"], nombre=er["nombre"]))

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
        return medico

    def get_all(self):
        query = "SELECT * FROM medico"
        medicos_data = self.db.execute_query(query, fetch=True)
        medicos = []
        if not medicos_data:
            return medicos

        # Para eficiencia, cargamos todas las asociaciones y especialidades en batch
        medico_ids = [r['id'] for r in medicos_data]
        # cargar asociaciones
        q_assoc = f"SELECT id_medico, id_especialidad FROM medico_x_especialidad WHERE id_medico IN ({', '.join(['%s']*len(medico_ids))})"
        assoc_rows = self.db.execute_query(q_assoc, tuple(medico_ids), fetch=True) or []
        esp_map = {}  # medico_id -> [esp_id,...]
        for a in assoc_rows:
            esp_map.setdefault(a['id_medico'], []).append(a['id_especialidad'])

        # cargar todas las especialidades necesarias
        all_esp_ids = sorted({eid for ids in esp_map.values() for eid in ids})
        esp_by_id = {}
        if all_esp_ids:
            q_esp = f"SELECT * FROM especialidad WHERE id IN ({', '.join(['%s']*len(all_esp_ids))})"
            esp_rows = self.db.execute_query(q_esp, tuple(all_esp_ids), fetch=True) or []
            for er in esp_rows:
                esp_by_id[er['id']] = Especialidad(id=er['id'], nombre=er['nombre'])

        # cargar usuarios (opcional) en batch
        user_ids = sorted({r['id_usuario'] for r in medicos_data if r.get('id_usuario')})
        users_by_id = {}
        if user_ids:
            q_u = f"SELECT * FROM usuario WHERE id IN ({', '.join(['%s']*len(user_ids))})"
            u_rows = self.db.execute_query(q_u, tuple(user_ids), fetch=True) or []
            for ur in u_rows:
                users_by_id[ur['id']] = Usuario(id=ur['id'], nombre_usuario=ur['nombre_usuario'], contrasena=ur['contrasena'], tipo_usuario=None)

        # construir objetos Medico
        for row in medicos_data:
            esp_list = []
            for eid in esp_map.get(row['id'], []):
                if eid in esp_by_id:
                    esp_list.append(esp_by_id[eid])
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
            SET nombre=%s, apellido=%s, dni=%s, matricula=%s, telefono=%s, mail=%s, direccion=%s, id_usuario=%s
            WHERE id=%s
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

        # reemplazar asociaciones: borramos las existentes y agregamos las nuevas
        try:
            self.mxesp_repo.remove_all_for_medico(medico.id)
            if medico.especialidades:
                for esp in medico.especialidades:
                    self.mxesp_repo.add(medico.id, esp.id)
        except Exception as e:
            print(f"❌ Error al modificar asociaciones de especialidades para medico {medico.id}: {e}")

        return self.get_by_id(medico.id)

    def delete(self, medico: Medico):
        # borrar asociaciones primero
        try:
            self.mxesp_repo.remove_all_for_medico(medico.id)
        except Exception as e:
            print(f"❌ Error al borrar asociaciones de medico {medico.id}: {e}")
        # borrar medico
        return self.db.execute_query("DELETE FROM medico WHERE id = %s", (medico.id,))

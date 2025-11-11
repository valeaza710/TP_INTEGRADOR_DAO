from backend.data_base.connection import DataBaseConnection
from backend.clases.paciente import Paciente
from backend.clases.usuario import Usuario
from backend.repository.repository import Repository

class PacienteRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, paciente: Paciente):
        query = """
            INSERT INTO paciente (nombre, apellido, dni, edad, fecha_nacimiento, mail, telefono, direccion, id_usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        user_id = paciente.usuario.id if paciente.usuario else None

        params = (
            paciente.nombre,
            paciente.apellido,
            paciente.dni,
            paciente.edad,
            paciente.fecha_nacimiento,
            paciente.mail,
            paciente.telefono,
            paciente.direccion,
            user_id,
        )

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            paciente.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return paciente
        except Exception as e:
            print(f"❌ Error al guardar paciente: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_by_id(self, paciente_id: int):
        query = "SELECT * FROM paciente WHERE id = ?"
        data = self.db.execute_query(query, (paciente_id,), fetch=True)
        if not data:
            return None
        row = data[0]

        # Cargar usuario si existe
        usuario = None
        if row.get("id_usuario"):
            usuario_data = self.db.execute_query("SELECT * FROM usuario WHERE id = ?", (row["id_usuario"],), fetch=True)
            if usuario_data:
                u = usuario_data[0]
                usuario = Usuario(id=u["id"], nombre_usuario=u["nombre_usuario"], contrasena=u["contrasena"], tipo_usuario=None)

        return Paciente(
            id=row["id"],
            nombre=row["nombre"],
            apellido=row["apellido"],
            dni=row["dni"],
            edad=row["edad"],
            fecha_nacimiento=row["fecha_nacimiento"],
            mail=row["mail"],
            telefono=row["telefono"],
            direccion=row["direccion"],
            usuario=usuario
        )

    def get_all(self):
        query = "SELECT * FROM paciente"
        pacientes_data = self.db.execute_query(query, fetch=True)
        pacientes = []

        if pacientes_data:
            for row in pacientes_data:
                usuario = None
                if row.get("id_usuario"):
                    usuario_data = self.db.execute_query("SELECT * FROM usuario WHERE id = ?", (row["id_usuario"],), fetch=True)
                    if usuario_data:
                        u = usuario_data[0]
                        usuario = Usuario(id=u["id"], nombre_usuario=u["nombre_usuario"], contrasena=u["contrasena"], tipo_usuario=None)

                pacientes.append(Paciente(
                    id=row["id"],
                    nombre=row["nombre"],
                    apellido=row["apellido"],
                    dni=row["dni"],
                    edad=row["edad"],
                    fecha_nacimiento=row["fecha_nacimiento"],
                    mail=row["mail"],
                    telefono=row["telefono"],
                    direccion=row["direccion"],
                    usuario=usuario
                ))
        return pacientes

    def modify(self, paciente: Paciente):
        query = """
            UPDATE paciente
            SET nombre=?, apellido=?, dni=?, edad=?, fecha_nacimiento=?, mail=?, telefono=?, direccion=?, id_usuario=?
            WHERE id=?
        """
        user_id = paciente.usuario.id if paciente.usuario else None
        params = (
            paciente.nombre,
            paciente.apellido,
            paciente.dni,
            paciente.edad,
            paciente.fecha_nacimiento,
            paciente.mail,
            paciente.telefono,
            paciente.direccion,
            user_id,
            paciente.id
        )

        success = self.db.execute_query(query, params)
        return paciente if success else None

    def delete(self, paciente: Paciente):
        query = "DELETE FROM paciente WHERE id = ?"
        return self.db.execute_query(query, (paciente.id,))

    def search_by_dni(self, dni_parcial: str):
        query = "SELECT * FROM paciente WHERE dni LIKE ?"
        pacientes_data = self.db.execute_query(query, (f'%{dni_parcial}%',), fetch=True)
        pacientes = []

        if pacientes_data:
            for row in pacientes_data:
                usuario = None
                if row.get("id_usuario"):
                    usuario_data = self.db.execute_query("SELECT * FROM usuario WHERE id = ?", (row["id_usuario"],), fetch=True)
                    if usuario_data:
                        u = usuario_data[0]
                        usuario = Usuario(id=u["id"], nombre_usuario=u["nombre_usuario"], contrasena=u["contrasena"], tipo_usuario=None)

                pacientes.append(Paciente(
                    id=row["id"],
                    nombre=row["nombre"],
                    apellido=row["apellido"],
                    dni=row["dni"],
                    edad=row["edad"],
                    fecha_nacimiento=row["fecha_nacimiento"],
                    mail=row["mail"],
                    telefono=row["telefono"],
                    direccion=row["direccion"],
                    usuario=usuario
                ))

        return pacientes

    def get_by_dni(self, dni: str):
        query = "SELECT * FROM paciente WHERE dni = ?"
        data = self.db.execute_query(query, (dni,), fetch=True)
        if not data:
            return None

        row = data[0]
        return Paciente(
            id=row["id"],
            nombre=row["nombre"],
            dni=row["dni"],
            fecha_nacimiento=row["fecha_nacimiento"]
        )

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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        if paciente.usuario == None:
            user = None
        else:
            user = paciente.usuario

        params = (
            paciente.nombre,
            paciente.apellido,
            paciente.dni,
            paciente.edad,
            paciente.fecha_nacimiento,
            paciente.mail,
            paciente.telefono,
            paciente.direccion,
            user,
        )

        conn = self.db.connect()
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
            return None

    def get_by_id(self, paciente_id: int):
        query = "SELECT * FROM paciente WHERE id = %s"
        data = self.db.execute_query(query, (paciente_id,), fetch=True)
        if not data:
            return None
        row = data[0]

        # Si el paciente tiene usuario asociado, lo cargamos
        usuario = None
        if row["id_usuario"]:
            usuario_data = self.db.execute_query("SELECT * FROM usuario WHERE id = %s", (row["id_usuario"],), fetch=True)
            if usuario_data:
                u = usuario_data[0]
                usuario = Usuario(u["id"], u["nombre_usuario"], u["contrasena"], u["rol"])

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
                if row["id_usuario"]:
                    usuario_data = self.db.execute_query("SELECT * FROM usuario WHERE id = %s", (row["id_usuario"],), fetch=True)
                    if usuario_data:
                        u = usuario_data[0]
                        usuario = Usuario(u["id"], u["nombre_usuario"], u["contrasena"], u["rol"])

                paciente = Paciente(
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
                pacientes.append(paciente)
        return pacientes

    def modify(self, paciente: Paciente):
        query = """
            UPDATE paciente SET nombre=%s, apellido=%s, dni=%s, edad=%s, fecha_nacimiento=%s,
                                mail=%s, telefono=%s, direccion=%s, id_usuario=%s
            WHERE id=%s
        """
        params = (
            paciente.nombre,
            paciente.apellido,
            paciente.dni,
            paciente.edad,
            paciente.fecha_nacimiento,
            paciente.mail,
            paciente.telefono,
            paciente.direccion,
            paciente.id
        )

        success = self.db.execute_query(query, params)
        return paciente if success else None

    def delete(self, paciente: Paciente):
        query = "DELETE FROM paciente WHERE id = %s"
        success = self.db.execute_query(query, (paciente.id,))
        return success

    # """Buscar pacientes por coincidencia parcial de DNI"""
    def search_by_dni(self, dni_parcial: str):
        query = "SELECT * FROM paciente WHERE CAST(dni AS CHAR) LIKE %s"
        pacientes_data = self.db.execute_query(query, (f'%{dni_parcial}%',), fetch=True)
        pacientes = []

        if pacientes_data:
            for row in pacientes_data:
                usuario = None
                if row["id_usuario"]:
                    usuario_data = self.db.execute_query("SELECT * FROM usuario WHERE id = %s", (row["id_usuario"],), fetch=True)
                    if usuario_data:
                        u = usuario_data[0]
                        usuario = Usuario(u["id"], u["nombre_usuario"], u["contrasena"], u["rol"])

                paciente = Paciente(
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
                pacientes.append(paciente)

        return pacientes

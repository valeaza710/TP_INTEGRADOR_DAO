# backend/repository/paciente_repository.py
from backend.data_base.connection import DataBaseConnection
from backend.clases.paciente import Paciente
from backend.repository.repository import Repository

class PacienteRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, paciente: Paciente):
        """Guardar nuevo paciente"""
        query = """
            INSERT INTO paciente (nombre, apellido, dni, edad, fecha_nacimiento, mail, telefono, direccion, id_usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            paciente.id_usuario
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
            paciente.id = cursor.lastrowid
            print(f"✅ Paciente '{paciente.nombre} {paciente.apellido}' guardado con ID: {paciente.id}")
            return paciente
        except Exception as e:
            print(f"❌ Error al guardar paciente: {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def get_by_dni(self, dni: str):
        """Buscar paciente por DNI"""
        query = "SELECT * FROM paciente WHERE dni = ?"
        data = self.db.execute_query(query, (dni,), fetch=True)
        if not data:
            return None
        return self._build_paciente(data[0])

    def get_by_mail(self, mail: str):
        """Buscar paciente por mail"""
        query = "SELECT * FROM paciente WHERE mail = ?"
        data = self.db.execute_query(query, (mail,), fetch=True)
        if not data:
            return None
        return self._build_paciente(data[0])

    def get_by_id_usuario(self, id_usuario: int):
        """Buscar paciente por ID de usuario"""
        query = "SELECT * FROM paciente WHERE id_usuario = ?"
        data = self.db.execute_query(query, (id_usuario,), fetch=True)
        if not data:
            return None
        return self._build_paciente(data[0])

    def get_by_id(self, paciente_id: int):
        """Buscar paciente por ID"""
        query = "SELECT * FROM paciente WHERE id = ?"
        data = self.db.execute_query(query, (paciente_id,), fetch=True)
        if not data:
            return None
        return self._build_paciente(data[0])

    def get_all(self):
        """Obtener todos los pacientes"""
        query = "SELECT * FROM paciente"
        pacientes_data = self.db.execute_query(query, fetch=True)
        pacientes = []

        if pacientes_data:
            for row in pacientes_data:
                paciente = self._build_paciente(row)
                if paciente:
                    pacientes.append(paciente)
        return pacientes

    def modify(self, paciente: Paciente):
        """Actualizar paciente"""
        query = """
            UPDATE paciente 
            SET nombre = ?, apellido = ?, dni = ?, edad = ?, 
                fecha_nacimiento = ?, mail = ?, telefono = ?, direccion = ?
            WHERE id = ?
        """
        params = (
            paciente.nombre,
            paciente.apellido,
            paciente.dni,
            paciente.edad,
            paciente.fecha_nacimiento,
            paciente.email,
            paciente.telefono,
            paciente.direccion,
            paciente.id
        )

        success = self.db.execute_query(query, params)
        return paciente if success else None

    def delete(self, paciente: Paciente):
        """Eliminar paciente"""
        query = "DELETE FROM paciente WHERE id = ?"
        success = self.db.execute_query(query, (paciente.id,))
        return success

    def _build_paciente(self, row):
        """Construir objeto Paciente desde una fila de BD"""
        return Paciente(
            id=row["id"],
            nombre=row.get("nombre"),
            apellido=row.get("apellido"),
            dni=row.get("dni"),
            edad=row.get("edad"),
            fecha_nacimiento=row.get("fecha_nacimiento"),
            mail=row.get("mail"),
            telefono=row.get("telefono"),
            direccion=row.get("direccion"),
            id_usuario=row.get("id_usuario")
        )
    
    def get_by_email(self, mail: str):
        """Buscar paciente por mail"""
        query = "SELECT * FROM paciente WHERE mail = ?"
        data = self.db.execute_query(query, (mail,), fetch=True)
        if not data:
            return None
        return self._build_paciente(data[0])

    def get_by_dni_nofunciono(self, dni: str):
        """Buscar paciente por DNI"""
        query = "SELECT * FROM paciente WHERE dni = ?"
        data = self.db.execute_query(query, (dni,), fetch=True)
        if not data:
            return None
        return self._build_paciente(data[0])
    

    def get_by_dni(self, dni_parcial: str):
        query = """
            SELECT id, nombre, apellido, dni, id_usuario, fecha_nacimiento, mail, telefono, direccion
            FROM paciente
            WHERE dni LIKE ?
        """
        param = (f"%{dni_parcial}%",)
        resultados = self.db.execute_query(query, param, fetch=True)  # Supongo que devuelve lista de tuplas o diccionarios
        pacientes = []
        for r in resultados:
            pacientes.append(Paciente(
                id=r['id'],
                nombre=r['nombre'],
                apellido=r['apellido'],
                dni=r['dni'],
                id_usuario=r['id_usuario'],
                fecha_nacimiento=r['fecha_nacimiento'],
                mail=r.get('mail'),
                telefono=r.get('telefono'),
                direccion=r.get('direccion')
            ))
        return pacientes
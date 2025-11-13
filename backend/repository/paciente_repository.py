from backend.data_base.connection import DataBaseConnection
from backend.clases.paciente import Paciente
from backend.repository.repository import Repository
from backend.clases.usuario import Usuario

class PacienteRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    # ------------------------------
    # CREATE
    # ------------------------------
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

    # ------------------------------
    # READ
    # ------------------------------
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

    def get_by_id(self, paciente_id: int):
        """Buscar paciente por ID"""
        query = "SELECT * FROM paciente WHERE id = ?"
        data = self.db.execute_query(query, (paciente_id,), fetch=True)
        if not data:
            return None
        return self._build_paciente(data[0])

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

    # ------------------------------
    # UPDATE
    # ------------------------------
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
            paciente.mail,
            paciente.telefono,
            paciente.direccion,
            paciente.id
        )

        success = self.db.execute_query(query, params)
        return paciente if success else None

    # ------------------------------
    # DELETE
    # ------------------------------
    def delete(self, paciente: Paciente):
        """Eliminar paciente"""
        query = "DELETE FROM paciente WHERE id = ?"
        success = self.db.execute_query(query, (paciente.id,))
        return success

    # ------------------------------
    # PRIVATE BUILDER
    # ------------------------------
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
    
    # ------------------------------
    # LOGIN
    # ------------------------------
    def get_paciente_id_by_credentials(self, username: str, password: str):
        """
        Verifica credenciales del usuario y, si es un paciente, 
        devuelve su ID de paciente.
        """
        # 1. Verificar credenciales del usuario
        usuario = self.usuario_repo.get_by_username_and_password(username, password)
        
        if not usuario:
            print(f"❌ Login fallido para usuario: {username}")
            return None # Credenciales incorrectas

        # 2. Si el usuario existe, obtener el paciente asociado
        paciente = self.get_by_id_usuario(usuario.id)
        
        if not paciente:
            print(f"⚠️ Usuario {username} (ID: {usuario.id}) no tiene registro de paciente asociado.")
            # Esto puede pasar si el usuario es un médico, secretario o administrador.
            return None 
            
        # 3. Devolver el ID REAL del paciente
        print(f"✅ Login exitoso. Paciente ID: {paciente.id}")
        return paciente.id


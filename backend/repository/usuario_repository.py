# backend/repository/usuario_repository.py
from backend.data_base.connection import DataBaseConnection
from backend.clases.usuario import Usuario
from backend.clases.tipo_usuario import TipoUsuario
from backend.repository.repository import Repository


class UsuarioRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, usuario: Usuario):
        """Guardar nuevo usuario (SOLO credenciales)"""
        query = """
            INSERT INTO usuario (nombre_usuario, contrasena, id_tipo_usuario)
            VALUES (?, ?, ?)
        """

        tipo_id = usuario.tipo_usuario.id if usuario.tipo_usuario else None
        params = (usuario.nombre_usuario, usuario.contrasena, tipo_id)

        conn = self.db.connect()
        if not conn:
            print("❌ Error al conectar con la base de datos.")
            return None

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            usuario.id = cursor.lastrowid
            print(f"✅ Usuario '{usuario.nombre_usuario}' guardado con ID: {usuario.id}")
            return usuario
        except Exception as e:
            print(f"❌ Error al guardar usuario: {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def get_by_username(self, nombre_usuario: str):
        """Buscar usuario por nombre de usuario"""
        query = "SELECT * FROM usuario WHERE nombre_usuario = ?"
        data = self.db.execute_query(query, (nombre_usuario,), fetch=True)
        if not data:
            return None
        return self._build_usuario(data[0])
    



    def get_by_id(self, usuario_id: int):
        """Buscar usuario por ID"""
        query = "SELECT * FROM usuario WHERE id = ?"
        data = self.db.execute_query(query, (usuario_id,), fetch=True)
        if not data:
            return None

        return self._build_usuario(data[0])

    def get_all(self):
        """Obtener todos los usuarios"""
        query = "SELECT * FROM usuario"
        usuarios_data = self.db.execute_query(query, fetch=True)
        usuarios = []

        if usuarios_data:
            for row in usuarios_data:
                usuario = self._build_usuario(row)
                if usuario:
                    usuarios.append(usuario)
        return usuarios

    def modify(self, usuario: Usuario):
        """Actualizar usuario"""
        query = """
            UPDATE usuario 
            SET nombre_usuario = ?, contrasena = ?, id_tipo_usuario = ?
            WHERE id = ?
        """
        tipo_id = usuario.tipo_usuario.id if usuario.tipo_usuario else None
        params = (usuario.nombre_usuario, usuario.contrasena, tipo_id, usuario.id)

        success = self.db.execute_query(query, params)
        return usuario if success else None

    def delete(self, usuario: Usuario):
        """Eliminar usuario"""
        query = "DELETE FROM usuario WHERE id = ?"
        success = self.db.execute_query(query, (usuario.id,))
        return success

    def _build_usuario(self, row):
        """Construir objeto Usuario desde una fila de BD"""
        tipo_usuario = None
        if row.get("id_tipo_usuario"):
            tipo_data = self.db.execute_query(
                "SELECT * FROM tipo_usuario WHERE id = ?",
                (row["id_tipo_usuario"],),
                fetch=True
            )
            if tipo_data:
                t = tipo_data[0]
                tipo_usuario = TipoUsuario(t["id"], t["tipo"])

        return Usuario(
            id=row["id"],
            nombre_usuario=row["nombre_usuario"],
            contrasena=row["contrasena"],
            tipo_usuario=tipo_usuario
        )
    
    # ... (dentro de la clase UsuarioRepository)

    def get_by_username_and_password(self, nombre_usuario: str, contrasena: str):
        """
        Busca un usuario por nombre de usuario y contraseña.
        ⚠️ Se recomienda usar hashing (ej: bcrypt) para contraseñas en un entorno real.
        """
        query = "SELECT * FROM usuario WHERE nombre_usuario = ? AND contrasena = ?"
        params = (nombre_usuario, contrasena)
        
        data = self.db.execute_query(query, params, fetch=True)
        if not data:
            return None
            
        return self._build_usuario(data[0])




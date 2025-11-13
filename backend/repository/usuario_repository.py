from backend.data_base.connection import DataBaseConnection
from backend.clases.usuario import Usuario
from backend.clases.tipo_usuario import TipoUsuario
from backend.repository.repository import Repository


class UsuarioRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, usuario: Usuario):
        query = """
            INSERT INTO usuario (nombre_usuario, contrasena, tipo_usuario)
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
            return usuario
        except Exception as e:
            print(f"❌ Error al guardar usuario: {e}")
            conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

    def get_by_id(self, usuario_id: int):
        query = "SELECT * FROM usuario WHERE id = ?"
        data = self.db.execute_query(query, (usuario_id,), fetch=True)
        if not data:
            return None
        row = data[0]

        tipo_usuario = None
        if row["tipo_usuario"]:
            tipo_data = self.db.execute_query(
                "SELECT * FROM tipo_usuario WHERE id = ?", (row["tipo_usuario"],), fetch=True
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

    def get_all(self):
        query = "SELECT * FROM usuario"
        usuarios_data = self.db.execute_query(query, fetch=True)
        usuarios = []

        if usuarios_data:
            for row in usuarios_data:
                tipo_usuario = None
                if row["id_tipo_usuario"]:
                    tipo_data = self.db.execute_query(
                        "SELECT * FROM tipo_usuario WHERE id = ?", (row["id_tipo_usuario"],), fetch=True
                    )
                    if tipo_data:
                        t = tipo_data[0]
                        tipo_usuario = TipoUsuario(t["id"], t["tipo"])

                usuario = Usuario(
                    id=row["id"],
                    nombre_usuario=row["nombre_usuario"],
                    contrasena=row["contrasena"],
                    tipo_usuario=tipo_usuario
                )
                usuarios.append(usuario)
        return usuarios

    def modify(self, usuario: Usuario):
        query = """
            UPDATE usuario 
            SET nombre_usuario = ?, contrasena = ?, tipo_usuario = ?
            WHERE id = ?
        """
        tipo_id = usuario.tipo_usuario.id if usuario.tipo_usuario else None
        params = (usuario.nombre_usuario, usuario.contrasena, tipo_id, usuario.id)

        success = self.db.execute_query(query, params)
        return usuario if success else None

    def delete(self, usuario: Usuario):
        query = "DELETE FROM usuario WHERE id = ?"
        success = self.db.execute_query(query, (usuario.id,))
        return success
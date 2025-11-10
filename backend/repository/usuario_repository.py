from data_base.connection import DataBaseConnection
from clases.usuario import Usuario
from clases.tipo_usuario import TipoUsuario
from repository.repository import Repository

class UsuarioRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, usuario: Usuario):
        query = """
            INSERT INTO usuario (nombre_usuario, contrasena, rol)
            VALUES (%s, %s, %s)
        """
        rol_id = usuario.tipo_usuario.id if usuario.tipo_usuario else None
        params = (usuario.nombre_usuario, usuario.contrasena, rol_id)

        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            usuario.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return usuario
        except Exception as e:
            print(f"❌ Error al guardar usuario: {e}")
            return None

    def get_by_id(self, usuario_id: int):
        query = "SELECT * FROM usuario WHERE id = %s"
        data = self.db.execute_query(query, (usuario_id,), fetch=True)
        if not data:
            return None
        row = data[0]

        tipo_usuario = None
        if row["rol"]:
            tipo_data = self.db.execute_query("SELECT * FROM tipo_usuario WHERE id = %s", (row["rol"],), fetch=True)
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
                if row["rol"]:
                    tipo_data = self.db.execute_query("SELECT * FROM tipo_usuario WHERE id = %s", (row["rol"],), fetch=True)
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
            SET nombre_usuario=%s, contrasena=%s, rol=%s
            WHERE id=%s
        """
        rol_id = usuario.tipo_usuario.id if usuario.tipo_usuario else None
        params = (usuario.nombre_usuario, usuario.contrasena, rol_id, usuario.id)

        success = self.db.execute_query(query, params)
        return usuario if success else None

    def delete(self, usuario: Usuario):
        query = "DELETE FROM usuario WHERE id = %s"
        success = self.db.execute_query(query, (usuario.id,))
        return success

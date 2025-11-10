from backend.data_base.connection import DataBaseConnection
from backend.clases.tipo_usuario import TipoUsuario
from backend.repository.repository import Repository

class TipoUsuarioRepository(Repository):
    def __init__(self):
        self.db = DataBaseConnection()

    def save(self, tipo_usuario: TipoUsuario):
        query = "INSERT INTO tipo_usuario (tipo) VALUES (%s)"
        params = (tipo_usuario.tipo,)
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            tipo_usuario.id = cursor.lastrowid
            cursor.close()
            conn.close()
            return tipo_usuario
        except Exception as e:
            print(f"❌ Error al guardar tipo de usuario: {e}")
            return None

    def get_by_id(self, tipo_usuario_id: int):
        query = "SELECT * FROM tipo_usuario WHERE id = %s"
        data = self.db.execute_query(query, (tipo_usuario_id,), fetch=True)
        if not data:
            return None
        row = data[0]
        return TipoUsuario(id=row["id"], tipo=row["tipo"])

    def get_all(self):
        query = "SELECT * FROM tipo_usuario"
        tipos_data = self.db.execute_query(query, fetch=True)
        tipos = []
        if tipos_data:
            for row in tipos_data:
                tipos.append(TipoUsuario(id=row["id"], tipo=row["tipo"]))
        return tipos

    def modify(self, tipo_usuario: TipoUsuario):
        query = "UPDATE tipo_usuario SET tipo = %s WHERE id = %s"
        params = (tipo_usuario.tipo, tipo_usuario.id)
        success = self.db.execute_query(query, params)
        return tipo_usuario if success else None

    def delete(self, tipo_usuario: TipoUsuario):
        query = "DELETE FROM tipo_usuario WHERE id = %s"
        success = self.db.execute_query(query, (tipo_usuario.id,))
        return success

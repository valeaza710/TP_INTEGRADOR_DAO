import mysql.connector
from mysql.connector import Error

class DataBaseConnection:
    def __init__(self, host="127.0.0.1", user="root", password="1234", database="tpdaobd", port="3310"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset="armscii8",
                collation="armscii8_bin"
            )
            return conn
        except Error as e:
            print(f"❌ Error al conectar con la base de datos: {e}")
            return None

    def execute_query(self, query, params=None, fetch=False):
        conn = self.connect()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"❌ Error en la ejecución SQL: {e}")
            return None



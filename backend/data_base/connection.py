import sqlite3
import os
from threading import Lock

class DataBaseConnection:
    _instance = None       # Guarda la instancia única
    _lock = Lock()         # Evita problemas en entornos multihilo

    def __new__(cls, db_name="tpdaobd.sqlite"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DataBaseConnection, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_name="tpdaobd.sqlite"):
        if self._initialized:
            return  # Evita re-inicializar la instancia
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self._initialized = True

    def connect(self):
        """Crea una conexión nueva hacia la base de datos SQLite."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Permite acceder por nombre de columna
            return conn
        except sqlite3.Error as e:
            print(f"❌ Error al conectar con la base de datos: {e}")
            return None

    def execute_query(self, query, params=None, fetch=False, script=False):
        """Ejecuta una consulta o script en la base de datos."""
        conn = self.connect()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            if script:
                cursor.executescript(query)
            else:
                cursor.execute(query, params or [])
            if fetch:
                result = cursor.fetchall()
                conn.close()
                return [dict(row) for row in result]
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"❌ Error en la ejecución SQL: {e}")
            return None
# backend/clases/usuario.py
from backend.clases.tipo_usuario import TipoUsuario

class Usuario:
    def __init__(self, 
                 id: int = None, 
                 nombre_usuario: str = None, 
                 contrasena: str = None,
                 tipo_usuario: TipoUsuario = None):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.tipo_usuario = tipo_usuario

    def __repr__(self):
        tipo = self.tipo_usuario.tipo if self.tipo_usuario else None
        return f"Usuario(id={self.id}, username='{self.nombre_usuario}', tipo='{tipo}')"
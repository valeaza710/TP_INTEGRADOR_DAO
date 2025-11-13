from backend.clases.usuario import Usuario

class Paciente:
    def __init__(self,
                 id: int = None,
                 nombre: str = None,
                 apellido: str = None,
                 dni: str = None,
                 edad: int = None,
                 fecha_nacimiento: str = None,
                 mail: str = None,
                 telefono: str = None,
                 direccion: str = None,
                 id_usuario: int = None,
                 usuario: Usuario = None):  # ✅ nuevo atributo
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.edad = edad
        self.fecha_nacimiento = fecha_nacimiento
        self.mail = mail
        self.telefono = telefono
        self.direccion = direccion
        self.id_usuario = id_usuario
        self.usuario = usuario  # ✅ nuevo atributo

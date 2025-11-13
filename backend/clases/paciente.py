class Paciente:
    def __init__(self,
                 id: int = None,
                 nombre: str = None,
                 apellido: str = None,
                 dni: str = None,
                 edad: int = None,
                 fecha_nacimiento: str = None,
                 mail: str = None,  # ← Cambiar de 'mail' a 'email'
                 telefono: str = None,
                 direccion: str = None,
                 id_usuario: int = None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.edad = edad
        self.fecha_nacimiento = fecha_nacimiento
        self.mail = mail  # ← Cambiar aquí también
        self.telefono = telefono
        self.direccion = direccion
        self.id_usuario = id_usuario
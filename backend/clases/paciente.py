class Paciente:
    def __init__(self, id=None, nombre=None, apellido=None, dni=None, edad=None,
                 fecha_nacimiento=None, mail=None, telefono=None, direccion=None, usuario=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.edad = edad
        self.fecha_nacimiento = fecha_nacimiento
        self.mail = mail
        self.telefono = telefono
        self.direccion = direccion
        self.usuario = usuario

    def __str__(self):
        return f"{self.id} {self.nombre} {self.apellido} {self.dni}"

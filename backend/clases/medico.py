from typing import List
from clases.usuario import Usuario
from clases.especialidad import Especialidad

class Medico:
    def init(
        self,
        id: int = None,
        nombre: str = None,
        apellido: str = None,
        dni: str = None,
        matricula: str = None,
        telefono: str = None,
        mail: str = None,
        direccion: str = None,
        especialidades: List[Especialidad] = None,
        usuario: Usuario = None
    ):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.matricula = matricula
        self.telefono = telefono
        self.mail = mail
        self.direccion = direccion
        self.especialidades = especialidades or []
        self.usuario = usuario

    def repr(self):
        return (
            f"Medico(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', "
            f"dni='{self.dni}', matricula='{self.matricula}', telefono='{self.telefono}', "
            f"mail='{self.mail}', direccion='{self.direccion}', "
            f"especialidades={self.especialidades}, usuario={self.usuario})"
        )
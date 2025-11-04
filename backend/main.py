from backend.clases import *
from repository import *

especialidad_repository = EspecialidadRepository()
especialidad1 = Especialidad(1, "Cardiologia")
print(especialidad1)
especialidad_repository.save(especialidad1)
especialidad = especialidad_repository.get_all()
for especialidad in especialidad:
    print(especialidad)
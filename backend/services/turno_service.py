from  backend.repository.agenda_turno_repository import AgendaTurnoRepository
from backend.repository.especialidad_repository import EspecialidadRepository


# backend/services/turno_service.py
from backend.services.agenda_turno_service import AgendaTurnoService


class TurnoService:
    def __init__(self):
        self.agenda_service = AgendaTurnoService()
        self.agenda_repo = AgendaTurnoRepository() 
        self.especialidad_repo = EspecialidadRepository()
        

    # -----------------------------
    # Obtener todos los turnos
    # -----------------------------
    def get_all(self):
        turnos = self.agenda_service.get_all()
        lista = []

        for t in turnos:
            lista.append({
                "id": t["id"],
                "doctor": f"Dr. {t.get('doctor', 'Sin asignar')}",
                "especialidad": t.get("especialidad", "General"),
                "fecha": t["fecha"],
                "hora": t["hora"],
                "lugar": t.get("lugar", "Sin especificar"),
                "estado": "Pendiente",
                "paciente": t.get("paciente", "Sin paciente")
            })

        return lista

    # -----------------------------
    # Crear un turno
    # -----------------------------
    def create(self, data):
    # La AgendaTurnoService.create puede devolver una tupla (response, status) si falla O el objeto completo si es exitoso.
        resultado = self.agenda_service.create(data)
        
        # Si el resultado es una tupla, probablemente es un error
        if isinstance(resultado, tuple):
            # Esto pasa cuando AgendaTurnoService.create devuelve jsonify({"error": ...}), 404
            # Devolvemos la tupla para que el router la maneje
            return resultado
            
        return resultado # Retorna el objeto de turno guardado si es exitoso
        # -----------------------------


    # Eliminar turno
    # -----------------------------
    def delete(self, id):
        return self.agenda_service.delete(id)

    # -----------------------------
    # Obtener horarios disponibles
    # -----------------------------
    def get_available_slots(self, specialty_name=None, doctor_id_str=None, date_str=None):
            
            # 1. Obtener ID de Especialidad usando tu repositorio
            especialidad = self.especialidad_repo.get_by_nombre(specialty_name)
            if not especialidad:
                return []
            id_especialidad = especialidad.id 

            # 2. Preparar ID de Médico
            doctor_id = None
            if doctor_id_str and doctor_id_str != 'all' and doctor_id_str != 'null':
                try:
                    doctor_id = int(doctor_id_str)
                except ValueError:
                    pass 

            # 3. Consultar Slots (usa la nueva función del repositorio)
            turnos_encontrados = self.agenda_repo.get_slots_by_filters(
                id_especialidad, doctor_id, date_str
            )

            available_slots = []
            
            # 4. Filtrar por Estado (id_estado_turno = 1) y Formatear
            for t in turnos_encontrados:
                # Aquí está el filtro clave: SOLO el estado 1 (Disponible)
                if t["id_estado_turno"] == 5:  # Estado 5 = Disponible
                    available_slots.append({
                        "doctor_id": t['medico_id'],
                        "doctor": f"{t['medico_nombre']} {t['medico_apellido']}",
                        "time": t['hora'],
                        "date": t['fecha'],
                        "id_turno": t['id'], 
                        "id_horario_medico": t.get("id_horario_medico")
                    })
                    
            return available_slots
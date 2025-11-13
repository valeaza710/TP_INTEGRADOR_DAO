# backend/services/turno_service.py
from backend.services.agenda_turno_service import AgendaTurnoService

class TurnoService:
    def __init__(self):
        self.agenda_service = AgendaTurnoService()

    # -----------------------------
    # Obtener todos los turnos
    # -----------------------------
    def get_all(self):
        turnos = self.agenda_service.get_all()
        lista = []

        for t in turnos:
            # Convertimos la estructura simple que necesita el frontend
            lista.append({
                "id": t["id"],
                "doctor": f"Dr. {t.get('doctor', 'Sin asignar')}",
                "especialidad": t.get("especialidad", "General"),
                "fecha": t["fecha"],
                "hora": t["hora"],
                "lugar": t.get("lugar", "Sin especificar"),
                "estado": "Pendiente",  # o mapeá según estado_turno si querés
                "paciente": t.get("paciente", "Sin paciente")
            })

        return lista

    # -----------------------------
    # Crear un turno
    # -----------------------------
    def create(self, data):
        # Reutilizamos la lógica de AgendaTurnoService
        return self.agenda_service.create(data)

    # -----------------------------
    # Eliminar turno
    # -----------------------------
    def delete(self, id):
        return self.agenda_service.delete(id)

def get_available_slots(self, specialty=None, doctor_name=None, date=None):
    turnos = self.repo.get_all()  # Trae todos los turnos
    available = []

    for t in turnos:
        if t.fecha == date:
            continue  # Ya ocupado
        if doctor_name and t.horario_medico.medico.nombre + " " + t.horario_medico.medico.apellido != doctor_name:
            continue
        if specialty and t.horario_medico.medico.especialidad.nombre != specialty:
            continue
        
        available.append({
            "id_horario_medico": t.horario_medico.id,
            "doctor": f"Dr. {t.horario_medico.medico.nombre} {t.horario_medico.medico.apellido}",
            "time": t.hora,
            "location": f"Consultorio {t.horario_medico.id}"
        })

    return available

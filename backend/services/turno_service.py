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
        return self.agenda_service.create(data)

    # -----------------------------
    # Eliminar turno
    # -----------------------------
    def delete(self, id):
        return self.agenda_service.delete(id)

    # -----------------------------
    # Obtener horarios disponibles
    # -----------------------------
    def get_available_slots(self, specialty=None, doctor_name=None, date=None):
        """
        Retorna los horarios disponibles para la especialidad y fecha.
        """
        turnos = self.agenda_service.get_all()  # Todos los turnos actuales
        available = []

        for t in turnos:
            # Si ya hay turno en esa fecha, lo salteamos
            if t["fecha"] == date:
                continue

            # Filtrar por médico si se eligió uno
            full_doctor_name = f"{t.get('doctor', '').replace('Dr. ', '')}"
            if doctor_name and full_doctor_name != doctor_name:
                continue

            # Filtrar por especialidad si aplica
            if specialty and t.get("especialidad") != specialty:
                continue

            available.append({
                "id_horario_medico": t.get("id_horario_medico", t["id"]),
                "doctor": t.get("doctor", "Sin doctor"),
                "time": t.get("hora", "00:00"),
                "location": t.get("lugar", "Consultorio")
            })

        return available

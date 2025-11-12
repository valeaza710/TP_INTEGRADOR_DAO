from datetime import date, timedelta
from backend.data_base.connection import DataBaseConnection
from backend.clases.agenda_turno import AgendaTurno
from backend.clases.paciente import Paciente

class NotificacionRepository:
    def __init__(self):
        self.db = DataBaseConnection()

def get_turnos_para_manana(self):
    # Fecha de mañana en formato YYYY-MM-DD
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    #OJO QUE ACA SUPONGO QUE EL ESTADO CON ID 2 ES EL DE ASIGNADO
    query = """
        SELECT 
            at.id, 
            at.fecha, 
            at.hora, 
            at.id_paciente,
            p.nombre, 
            p.apellido, 
            p.mail, 
            p.telefono
        FROM agenda_turno at
        JOIN paciente p ON at.id_paciente = p.id
        WHERE date(at.fecha) = ?
          AND at.estado_turno = 2
    """

    rows = self.db.execute_query(query, (tomorrow,), fetch=True)
    turnos = []
    if not rows:
        return turnos

    for r in rows:
        paciente = Paciente(
            id=r["id_paciente"],
            nombre=r.get("nombre"),
            apellido=r.get("apellido"),
            mail=r.get("mail"),
            telefono=r.get("telefono")
        )
        turno = AgendaTurno(
            id=r["id"],
            fecha=r["fecha"],
            hora=r["hora"],
            paciente=paciente
        )
        turnos.append(turno)

    return turnos


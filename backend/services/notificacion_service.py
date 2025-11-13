from backend.repository.notificacion_repository import NotificacionRepository
from backend.utils.mailer import Mailer

class NotificacionService:
    def __init__(self):
        self.repo = NotificacionRepository()
        self.mailer = Mailer()

    def enviar_recordatorios_turnos(self):
        """Obtiene todos los turnos de mañana y envía recordatorios por correo."""
        turnos = self.repo.get_turnos_para_manana()
        if not turnos:
            print("📭 No hay turnos asignados para mañana.")
            return

        for turno in turnos:
            paciente = turno.paciente
            if not paciente.mail:
                print(f"⚠️ Paciente {paciente.nombre} {paciente.apellido} sin email.")
                continue

            asunto = "📅 Recordatorio de turno médico"
            cuerpo = (
                f"Hola {paciente.nombre},\n\n"
                f"Te recordamos que tenés un turno asignado para mañana "
                f"{turno.fecha} a las {turno.hora}.\n\n"
                "Por favor, confirmá tu asistencia o avisá si no podés asistir.\n\n"
                "¡Gracias!\n"
                "Centro Médico"
            )

            exito, error = self.mailer.send_mail(paciente.mail, asunto, cuerpo)
            if exito:
                print(f"✅ Mail enviado a {paciente.mail}")
            else:
                print(f"❌ Error al enviar a {paciente.mail}: {error}")

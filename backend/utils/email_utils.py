from backend.utils.mailer import Mailer

def enviar_mail(destinatario: str, asunto: str, cuerpo: str):
    """
    Envía un correo electrónico simple usando la clase Mailer.
    Las credenciales SMTP deben estar configuradas en variables de entorno:
    SMTP_USER, SMTP_PASS, SMTP_SERVER, SMTP_PORT
    """
    mailer = Mailer()
    exito, error = mailer.send_mail(destinatario, asunto, cuerpo)
    if not exito:
        raise Exception(f"Error enviando mail a {destinatario}: {error}")
    return True

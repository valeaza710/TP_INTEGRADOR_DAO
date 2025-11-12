import smtplib
from email.message import EmailMessage
import os

class Mailer:
    def __init__(self, smtp_server=None, smtp_port=None, user=None, password=None):
        self.smtp_server = smtp_server or os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(smtp_port or os.getenv("SMTP_PORT", 587))
        self.user = user or os.getenv("SMTP_USER")
        self.password = password or os.getenv("SMTP_PASS")

    def send_mail(self, to_email: str, subject: str, body: str):
        if not self.user or not self.password:
            raise RuntimeError("Mailer: faltan credenciales SMTP en env vars")

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.user
        msg["To"] = to_email
        msg.set_content(body)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=20) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
            return True, None
        except Exception as e:
            return False, str(e)

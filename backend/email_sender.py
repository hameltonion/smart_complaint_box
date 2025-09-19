import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class MockEmailSender:
    def send_email(self, subject: str, body: str, to_email: str):
        logger.info(f"MOCK EMAIL SENT\nTo: {to_email}\nSubject: {subject}\nBody: {body}")
        return True


class RealEmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password):
        self.server = smtp_server
        self.port = int(smtp_port)
        self.user = smtp_user
        self.password = smtp_password

    def send_email(self, subject: str, body: str, to_email: str):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.user
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP_SSL(self.server, self.port) as server:
                server.login(self.user, self.password)
                server.sendmail(self.user, to_email, msg.as_string())
            logger.info(f"📧 Real email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send email to {to_email}: {e}")
            return False


def get_email_sender():
    """
    Returns a real or mock email sender based on .env configs.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if all([smtp_server, smtp_port, smtp_user, smtp_password]):
        return RealEmailSender(smtp_server, smtp_port, smtp_user, smtp_password)

    logger.warning("⚠️ SMTP configs missing — using MockEmailSender")
    return MockEmailSender()
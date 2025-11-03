import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.relay import tag_subject

logger = logging.getLogger(__name__)

def get_email_sender():
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
        logger.warning("Email environment variables are not set. Using mock sender.")
        return MockEmailSender()
    return RealEmailSender(smtp_server, smtp_port, smtp_user, smtp_password)

class MockEmailSender:
    def send_email(self, subject: str, body: str, to_email: str):
        subject = tag_subject(subject)
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
            subject = tag_subject(subject)

            msg = MIMEMultipart()
            msg["From"] = self.user
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.user, to_email, msg.as_string())

            logger.info(f"✅ Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send email to {to_email}: {e}")
            return False
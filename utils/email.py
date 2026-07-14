import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings

def send_email(email_to: str, subject: str, message: str):
    """
    Email sender. Sends a real email if SMTP settings are configured.
    Otherwise, prints to console as a mock email for development.
    """
    if settings.SMTP_SERVER and settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_FROM_EMAIL
            msg['To'] = email_to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"REAL EMAIL SENT TO: {email_to}")
            return
        except Exception as e:
            print(f"Failed to send email via SMTP: {e}")
            # Fall back to mock email

    print("-" * 50)
    print(f"MOCK EMAIL SENT TO: {email_to}")
    print(f"SUBJECT: {subject}")
    print(f"MESSAGE:\n{message}")
    print("-" * 50)

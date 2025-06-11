from django.conf import settings
import environ
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from celery import shared_task


def _send_email_with_pdf(subject, message, sender_email, receiver_emails, pdf_bytes, pdf_name):

    # Preparing the message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_emails
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    # Adding pdf attachment
    pdf_part = MIMEApplication(pdf_bytes, _subtype='pdf')
    pdf_part.add_header('Content-Disposition', 'attachment', filename=pdf_name)
    msg.attach(pdf_part)

    # Setting up the mail server
    env = environ.Env()
    environ.Env.read_env()
    smtp_username = env('EMAIL_HOST_USER')
    smtp_password = env('EMAIL_HOST_PASSWORD')
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_HOST_PORT

    try:
        # Sending the message
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@shared_task
def send_cv_to_email(cv_pdf_content, cv_pdf_name, cv_name, cv_email):
    subject = f"DTEAM Test: {cv_name} CV Profile PDF"
    message = f"Please find {cv_name}'s CV attached"
    return _send_email_with_pdf(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        cv_email,
        cv_pdf_content,
        cv_pdf_name
    )

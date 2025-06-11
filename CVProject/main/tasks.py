from django.conf import settings
import smtplib
from celery import shared_task
import environ


def _send_email(subject, message, sender_email, receiver_emails):
    full_message = 'Subject: {}\n\n{}'.format(subject, message)

    env = environ.Env()
    environ.Env.read_env()
    smtp_username = env('EMAIL_HOST_USER')
    smtp_password = env('EMAIL_HOST_PASSWORD')
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_HOST_PORT

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_addr=sender_email, to_addrs=receiver_emails, msg=full_message)


@shared_task
def send_cv_to_email(cv_pdf, cv_name, cv_email):
    subject = f"DTEAM Test: {cv_name} CV Profile PDF"
    message = f"Please find {cv_name}'s CV attached"

    return _send_email(subject, message, settings.DEFAULT_FROM_EMAIL, [cv_email])

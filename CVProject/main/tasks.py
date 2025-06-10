from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_cv_to_email(cv_pdf, cv_name, cv_email):
    subject = f"DTEAM Test: {cv_name} CV Profile PDF"
    message = f"Please find {cv_name}'s CV attached"
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [cv_email])

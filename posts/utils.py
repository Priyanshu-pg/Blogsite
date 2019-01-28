from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_mail(request, email):
    subject = 'Confirmation mail'
    message = 'Hi there, you have been subscribed'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False
    )

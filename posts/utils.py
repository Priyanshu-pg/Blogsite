from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
import json

def send_mail_to(request, email):
    redirect_link = request.build_absolute_uri(reverse('confirm-subscriber', args=[email]))
    text_message = "Click "+redirect_link
    html_message = render_to_string('template_confirmation_mail.html', {'link': redirect_link})

    subject = 'Confirm Subscription'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    msg = EmailMultiAlternatives(subject, text_message, email_from, recipient_list)
    msg.attach_alternative(html_message, "text/html")
    if msg.send(fail_silently=False):
        # send_mail_to(request, current_email)
        return HttpResponse(
            json.dumps({"success_msg": "Email sent"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"error_msg": "Email could not be sent"}),
            content_type="application/json"
        )

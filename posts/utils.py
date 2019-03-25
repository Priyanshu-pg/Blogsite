from django.conf import settings

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
import json


def send_mail_to(request, email, hash_email):
    confirmation_link = request.build_absolute_uri(reverse('confirm-subscriber', args=[hash_email]))
    modify_link = request.build_absolute_uri(reverse('modify-subscription', args=[hash_email]))
    unsubscribe_link = request.build_absolute_uri(reverse('unsubscribe', args=[hash_email]))
    text_message = "Click "+confirmation_link
    html_message = render_to_string('template_confirmation_mail.html', {'confirmation_link': confirmation_link,
                                                                        'modify_link': modify_link,
                                                                        'unsubscribe_link': unsubscribe_link})

    subject = 'Confirm Subscription'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    msg = EmailMultiAlternatives(subject, text_message, email_from, recipient_list)
    msg.attach_alternative(html_message, "text/html")
    if msg.send(fail_silently=False):
        return HttpResponse(
            json.dumps({"success_msg": "Email sent"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"error_msg": "Email could not be sent"}),
            content_type="application/json"
        )

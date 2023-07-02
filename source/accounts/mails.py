from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
import smtplib
from celery import shared_task
from email.mime.text import MIMEText


def send_mail(to, template, context):
    html_content = render_to_string(f'emails/{template}', context)
    text_content = render_to_string(f'emails/{template}', context)
    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def send_created_account_mail(user):
    sender = 'accounts@inventorymanagement.local'
    receivers = ['test@mailhog.local'] 

    port = 1025

    header = "Account Created!\n"
    body = "Thank you for succesfully created your account on the intentory management app! \n User name: " + user.username +  " \n\n Enjoy!!" 

    msg = MIMEText(header + body)

    msg['Subject'] = 'Registration form'
    msg['From'] = sender
    msg['To'] = user.email
    
    with smtplib.SMTP('host.docker.internal', port) as server:
        server.sendmail(sender, receivers, msg.as_string())

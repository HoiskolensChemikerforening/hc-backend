from threading import Thread

from django.core.mail import send_mail
from mail_templated import send_mail
from post_office import mail

DEFAULT_FROM_EMAIL = 'Webkom@hc.ntnu.no'


def send_activation_mail(context, user_mail, template):
    print("SENDING MAIL")
    send_mail(template, context, DEFAULT_FROM_EMAIL, [user_mail])
    print("MAIL SENT")


def send_forgot_password_mail(request, email, user, token):
    template = 'profile_forgot_password'

    mail.send(
        email,  # List of email addresses also accepted
        DEFAULT_FROM_EMAIL,
        template=template,  # Could be an EmailTemplate instance or name
        context={'request': request, 'user': user, 'email': email, 'code': token},
        )

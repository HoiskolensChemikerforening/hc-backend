from threading import Thread
from django.core.mail import send_mail
from mail_templated import send_mail

DEFAULT_FROM_EMAIL = 'edb.ntnu@gmail.com'


def queue_activation_mail(context, template):
    locker_user = context['locker_user']
    if locker_user.internal_user:
        user_email = locker_user.internal_user.email
    else:
        user_email = locker_user.username

    thread = Thread(target=send_activation_mail, args=(context, user_email, template))
    thread.start()


def send_activation_mail(context, user_mail, template):
    print("SENDING MAIL")
    send_mail(template, context, DEFAULT_FROM_EMAIL, [user_mail])

    print("MAIL SENT")


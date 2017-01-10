from threading import Thread

from django.core.mail import send_mail
from mail_templated import send_mail
from post_office import mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def queue_activation_mail(context, template):
    user_email = context['locker_user'].username
    thread = Thread(target=send_activation_mail, args=(context, user_email, template))
    thread.start()


def send_activation_mail(context, user_mail, template):
    print("SENDING MAIL")
    send_mail(template, context, settings.DEFAULT_FROM_EMAIL, [user_mail])
    print("MAIL SENT")

def send_my_lockers_mail(email, lockers, user):
    template = 'lockers_mine_skap'

    mail.send(
        email,  # List of email addresses also accepted
        settings.DEFAULT_FROM_EMAIL,
        template=template,  # Could be an EmailTemplate instance or name
        context={'user': user, 'email': email, 'lockers': lockers},
        )
    return redirect(reverse('frontpage:home'))

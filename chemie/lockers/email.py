from post_office import mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def send_my_lockers_mail(email, lockers, user):
    template = 'lockers_my_lockers'

    mail.send(
        email,
        settings.DEFAULT_FROM_EMAIL,
        template=template,
        context={'user': user, 'email': email, 'lockers': lockers, 'root_url': get_current_site(None)},
        )


def send_activation_email(user, token, reactivation=False):
    if reactivation:
        template = 'lockers_reactivate'
    else:
        template = 'lockers_activate'

    mail.send(
        user.email,
        settings.DEFAULT_FROM_EMAIL,
        template=template,
        context={'user': user, 'email': user.email, 'ownership': token.ownership,
                 "token": token, 'root_url': get_current_site(None)},
    )

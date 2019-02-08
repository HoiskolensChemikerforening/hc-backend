from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from post_office import mail


def send_my_lockers_mail(email, lockers, user):
    template = "lockers_my_lockers"

    mail.send(
        email,
        settings.DEFAULT_FROM_EMAIL,
        template=template,
        context={
            "user": user,
            "email": email,
            "lockers": lockers,
            "root_url": get_current_site(None),
        },
    )


def send_final_warning(user, token):
    send_locker_email(user, token, activation_type="lockers_final_warning")


def send_re_activation_mail(user, token):
    send_locker_email(user, token, activation_type="lockers_reactivate")


def send_activation_mail(user, token):
    send_locker_email(user, token, activation_type="lockers_activate")


def send_locker_email(user, token, activation_type):
    mail.send(
        user.email,
        settings.DEFAULT_FROM_EMAIL,
        template=activation_type,
        context={
            "user": user,
            "email": user.email,
            "ownership": token.ownership,
            "token": token,
            "root_url": get_current_site(None),
        },
    )

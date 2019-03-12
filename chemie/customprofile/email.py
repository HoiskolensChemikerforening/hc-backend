from post_office import mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


def send_forgot_password_mail(email, user, token):
    template = "profile_forgot_password"
    mail.send(
        email,
        settings.DEFAULT_FROM_EMAIL,
        template=template,
        context={
            "user": user,
            "email": email,
            "code": token,
            "root_url": get_current_site(None),
        },
    )

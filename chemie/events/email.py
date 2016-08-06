from post_office import mail
from .models import REGISTRATION_STATUS


def send_event_mail(registration):
    if registration.status == REGISTRATION_STATUS.CONFIRMED:
        template = 'event_bekreftet_plass'
    else:
        template = 'event_på_venteliste'

    mail.send(
        registration.user.email, # List of email addresses also accepted
        'festkom@hc.ntnu.no',
        template=template, # Could be an EmailTemplate instance or name
        context={'event':registration.event, 'user':registration.user},
    )
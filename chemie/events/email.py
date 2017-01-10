from post_office import mail
from .models import REGISTRATION_STATUS


def send_event_mail(registration, event):
    template = 'event'
    mail.send(
        registration.user.email,  # List of email addresses also accepted
        'festkom@hc.ntnu.no',
        template=template,  # Could be an EmailTemplate instance or name
        context={
            'event': registration.event,
            'user': registration.user,
            'subject': event.title
        },
    )

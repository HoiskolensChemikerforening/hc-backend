from post_office import mail
from django.contrib.sites.shortcuts import get_current_site

def send_event_mail(registration, event):
    template = 'event'
    mail.send(
        registration.user.email,
        'pHaestkom <festkom@hc.ntnu.no>',
        template=template,
        context={
            'event': registration.event,
            'user': registration.user,
            'subject': event.title,
            'registration': registration,
            'root_url': get_current_site(None)
        },
    )

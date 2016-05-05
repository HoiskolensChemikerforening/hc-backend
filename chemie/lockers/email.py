from django.template.loader import render_to_string
from threading import Thread
from django.core.mail import send_mail
from django.conf import settings.EMAIL_HOST_USER



def send_activation_mail():
    email_subject = 'Bokskap - Aktivering'
    message = 'Congratulations! Your user is created. Activate your user account trough this link'
    email_message = render_to_string('signup_mail.html', {'request': request, 'message': message, 'hash_key': auth_object.key.hex})
    thread = Thread(target=send_password_email, args=(email_subject, email_message, email))
    thread.start()



def send_password_email(subject, message, email):
    print("SENDING MAIL")
    send_mail(subject,
              message,
              '%s'.format(EMAIL_HOST_USER),
              [email],
              fail_silently=False,
              html_message=message)

    print("MAIL SENT")
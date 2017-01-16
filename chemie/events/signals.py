from django.db.models.signals import post_save
from django.dispatch import receiver

from .email import send_event_mail
from .models import Event, BaseRegistration, REGISTRATION_STATUS
from .views import set_user_event_status


@receiver(post_save, sender=Event)
def post_save_event_receiver(sender, instance, *args, **kwargs):
    free_slots = instance.spare_slots
    potential_free = BaseRegistration.objects.filter(event=instance, status=REGISTRATION_STATUS.WAITING)
    potential_free = potential_free.order_by("-created")[0:free_slots]

    for lucky_registration in potential_free:
        status = set_user_event_status(instance, lucky_registration)
        if status == REGISTRATION_STATUS.CONFIRMED:
            send_event_mail(lucky_registration, instance)


post_save.connect(post_save_event_receiver, sender=Event)

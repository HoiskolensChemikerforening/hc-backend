from django.core.management.base import BaseCommand
from chemie.events.models import SocialReseller
from django.utils import timezone

class Command(BaseCommand):
    help = (
        "Command for contacting new potential buyers for event resales. "
    )

    def handle(self, *args, **options):

        ignored_offers = SocialReseller.objects.filter(deadline_lt=timezone.now())
   

        
        # Go through each rejected offer and try to contact a new seller
        for offer in ignored_offers:

            event = offer.registration.event 


from django.core.management.base import BaseCommand, CommandError
from lockers.models import Ownership, LockerConfirmation


class Command(BaseCommand):
    help = "Command for freeing inactive lockers that aren't (re)activated."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Pruning unconfirmed ownerships and tokens'))
        # Remove unconfirmed ownerships
        Ownership.objects.prune_expired()
        # Clear old tokens
        LockerConfirmation.objects.prune_expired()
        self.stdout.write(self.style.SUCCESS('Pruning complete.'))

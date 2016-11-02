from django.core.management.base import BaseCommand, CommandError
from lockers.models import Ownership
from lockers.email import queue_activation_mail


class Command(BaseCommand):
    help = "Command for resetting locker ownerships. " \
           "Every locker user will be prompted with an email for re-activation."

    def add_arguments(self, parser):
        parser.add_argument('--silent',
                            action='store_true',
                            dest='silent',
                            default=False,
                            help='Silently issue command',
                            )

    def handle(self, *args, **options):
        if not options.get('silent'):
            self.stdout.write(self.style.NOTICE(self.help))
            self.stdout.write(self.style.NOTICE('Are you sure you wish to proceed? y/N'))
            confirm = input('').lower()
            if confirm == 'y':
                self.stdout.write(self.style.SUCCESS('Resetting lockers...'))
            else:
                raise CommandError('Aborted.')
        else:
            self.stdout.write(self.style.NOTICE('Silent treatment received.'))

        reset_locker_ownerships()
        self.stdout.write(self.style.SUCCESS('Lockers reset'))


def reset_locker_ownerships():
    # Oh boi where to start... definite_owner is the related name between Ownership and
    # Locker, (Ownership -> Locker) it lets us collect all Lockers where "owner" definite link is set (__isnull=False).
    # Finally, we filter all ownerships that are connected to these Lockers (with its "weak" link)
    ownerships_to_reset = Ownership.objects.filter(definite_owner__owner__isnull=False).prefetch_related("user")

    for ownership in ownerships_to_reset:
        ownership.is_active = False
        ownership.save()
        confirmation_object = ownership.create_confirmation()

        context = {
            "confirmation": confirmation_object,
            "locker_user": ownership.user,
            "ownership": ownership,
        }
        queue_activation_mail(context, 'emails/reactivate.html')

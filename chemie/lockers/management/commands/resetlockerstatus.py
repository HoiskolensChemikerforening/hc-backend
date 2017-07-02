from django.core.management.base import BaseCommand, CommandError
from lockers.models import Ownership
from lockers.email import send_re_activation_mail


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

        lockers_reset = reset_locker_ownerships()
        self.stdout.write(self.style.SUCCESS('{} lockers reset'.format(lockers_reset)))


def reset_locker_ownerships():
    # Oh boi where to start... definite_owner is the related name between Ownership and
    # Locker, (Ownership -> Locker) it lets us collect all Lockers where "owner" definite link is set (__isnull=False).
    # Finally, we filter all ownerships that are connected to these Lockers (with its "weak" link)
    ownerships_to_reset = Ownership.objects.filter(definite_owner__owner__isnull=False).prefetch_related("user")

    for ownership in ownerships_to_reset:
        ownership.is_active = False
        ownership.save()
        token = ownership.create_confirmation()

        user = ownership.user
        send_re_activation_mail(user, token)

    return len(ownerships_to_reset)
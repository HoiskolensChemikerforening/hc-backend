from django.core.management.base import BaseCommand, CommandError
from lockers.models import Locker


class Command(BaseCommand):
    help = "Command for freeing inactive lockers that aren't (re)activated."

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
                self.stdout.write(self.style.NOTICE('Freeing lockers...'))
            else:
                raise CommandError('Aborted.')
        else:
            self.stdout.write(self.style.NOTICE('Silent treatment received.'))

        idle_lockers_count = Locker.objects.reset_idle()
        self.stdout.write(self.style.SUCCESS('{} lockers freed!'.format(idle_lockers_count)))

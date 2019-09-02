from django.core.management.base import BaseCommand, CommandError
from chemie.web_push.models import Device


class Command(BaseCommand):
    help = "Command for deleting inactive devices that aren't active"

    def add_arguments(self, parser):
        parser.add_argument(
            "--silent",
            action="store_true",
            dest="silent",
            default=False,
            help="Silently issue command",
        )

    def handle(self, *args, **options):
        if not options.get("silent"):
            self.stdout.write(self.style.NOTICE(self.help))
            self.stdout.write(
                self.style.NOTICE("Are you sure you wish to proceed? y/N")
            )
            confirm = input("").lower()
            if confirm == "y":
                self.stdout.write(self.style.NOTICE("deleting devices..."))
            else:
                raise CommandError("Aborted.")
        else:
            self.stdout.write(self.style.NOTICE("Silent treatment received."))
        delete_count = Device.delete_inactive_gcm_device()

        self.stdout.write(
            self.style.SUCCESS("{} devices deleted!".format(delete_count))
        )

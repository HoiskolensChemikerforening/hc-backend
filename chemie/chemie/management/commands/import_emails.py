import json
import os
from os.path import join
from subprocess import Popen, PIPE
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from post_office.models import EmailTemplate
from django.core import serializers
import subprocess


# Email template repo source directory
EMAIL_TEMPLATE_DIR = os.path.join(settings.BASE_DIR, "emails", "")



class Command(BaseCommand):
    help = (
        "Command for importing email HTML-files. "
        "Transpiles MJML to HTML and replaces all current EmailTemplates with updated HTML"
    )

    def import_email_template(self, **kwargs):
        directory = kwargs.pop("path")

        with open(f"{directory}.html", "r", encoding="utf-8") as html:
            kwargs["html_content"] = html.read()

        with open(f"{directory}.txt", "r", encoding="utf-8") as txt:
            kwargs["content"] = txt.read()

        EmailTemplate.objects.create(**kwargs)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(self.help))
        # Transpile all MJML-files
        transpiler = subprocess.run(
            ["bash", "-c", "./mjml-transpile.sh"],
            cwd=EMAIL_TEMPLATE_DIR,
            stdout=PIPE,
            stderr=PIPE,
        )

        message = str(transpiler.stdout.decode("utf-8"))
        if "MJMLError" in message:
            self.stdout.write(self.style.ERROR("MJML-transpiler failed!"))
            self.stdout.write(self.style.ERROR(message))
            return

        # Delete current templates from database
        EmailTemplate.objects.all().delete()

        with open(
            join(EMAIL_TEMPLATE_DIR, "email-structure.json"),
            "r",
            encoding="utf-8",
        ) as f:
            emails = json.load(f)

        # Reload each template file from email-structure.json and the
        # corresponding *.mjml (HTML) and *.txt (plain-text) files
        for email_data in emails:
            email_data["path"] = join(EMAIL_TEMPLATE_DIR, email_data["path"])
            self.import_email_template(**email_data)

        data = serializers.serialize("json", EmailTemplate.objects.all())

        with open(
            os.getcwd() + "/chemie/fixtures/email-templates.json", "w"
        ) as f:
            f.write(data)

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(emails)} email templates successfully loaded"
            )
        )

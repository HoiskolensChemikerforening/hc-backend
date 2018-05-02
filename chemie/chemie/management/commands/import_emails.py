import json
import os
from os.path import join
from subprocess import Popen, PIPE

from django.conf import settings
from django.core.management.base import BaseCommand
from post_office.models import EmailTemplate
from django.core import serializers


# Email template repo source directory
EMAIL_TEMPLATE_DIR = settings.BASE_DIR.path('emails').root


class Command(BaseCommand):
    help = "Command for importing email HTML-files. " \
           "Transpiles MJML to HTML and replaces all current EmailTemplates with updated HTML"

    def import_email_template(self, **kwargs):
        directory = kwargs.pop('path')

        with open(f'{directory}.html', 'r', encoding='utf-8') as html:
            kwargs['html_content'] = html.read()

        with open(f'{directory}.txt', 'r', encoding='utf-8') as txt:
            kwargs['content'] = txt.read()

        EmailTemplate.objects.create(**kwargs)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(self.help))
        # Transpile all MJML-files
        transpiler = Popen(f'cd {EMAIL_TEMPLATE_DIR} && bash -c ./mjml-transpile.sh', shell=True, stdout=PIPE,
                           stderr=PIPE, executable='/bin/bash')
        transpiler.wait()
        message = str(transpiler.stdout.read().decode("utf-8"))
        if 'MJMLError' in message:
            self.stdout.write(self.style.ERROR('MJML-transpiler failed!'))
            self.stdout.write(self.style.ERROR(message))
            return

        # Delete current templates from database
        EmailTemplate.objects.all().delete()

        with open(join(EMAIL_TEMPLATE_DIR, 'email-structure.json'), 'r', encoding='utf-8') as f:
            emails = json.load(f)

        # Reload each template file from email-structure.json and the
        # corresponding *.mjml (HTML) and *.txt (plain-text) files
        for email_data in emails:
            email_data['path'] = join(EMAIL_TEMPLATE_DIR, email_data['path'])
            self.import_email_template(**email_data)

        data = serializers.serialize("json", EmailTemplate.objects.all())
        with open(settings.BASE_DIR.path('chemie/fixtures/email-templates.json').root, "w") as f:
            f.write(data)

        self.stdout.write(self.style.SUCCESS(f'{len(emails)} email templates successfully loaded'))

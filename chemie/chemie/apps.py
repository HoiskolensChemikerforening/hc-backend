from __future__ import unicode_literals
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'chemie'

    def ready(self):
        from . import signals

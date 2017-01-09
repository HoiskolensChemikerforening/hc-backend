from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = 'events'
    verbose_name = 'Arrangementer - administrativt'

    def ready(self):
        import events.signals

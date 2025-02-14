from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = "chemie.events"
    verbose_name = "Arrangementer"

    def ready(self):
        import chemie.events.signals

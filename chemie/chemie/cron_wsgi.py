from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chemie.chemie.settings")

application = get_wsgi_application()

try:
    import uwsgidecorators
    from django.core.management import call_command

    @uwsgidecorators.timer(10)
    def send_queued_mail(num):
        """Send queued mail every 10 seconds"""
        call_command("send_queued_mail", processes=1)

    @uwsgidecorators.timer(60*30)
    def update_event_resale(num):
        """Find a new potential buyer for ignored offers every 30 minutes"""
        call_command("update_event_resale", processes=1)

except ImportError:
    print("uwsgidecorators not found. Cron and timers are disabled")

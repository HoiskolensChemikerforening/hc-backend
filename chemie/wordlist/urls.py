from django.urls import path
from .views import save_device, send_notification, CoffeeLatestSubmission

app_name = "wordlist"


urlpatterns = [
    path("", send_notification, name="send"),
]

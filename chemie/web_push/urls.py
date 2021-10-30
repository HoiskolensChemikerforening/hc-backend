from django.urls import path
from .views import save_device, send_notification, CoffeeLatestSubmission

app_name = "notifications"


urlpatterns = [
    path("send/", send_notification, name="send"),
    path("save/", save_device, name="save"),
    path("api/", CoffeeLatestSubmission.as_view(), name="api")
]

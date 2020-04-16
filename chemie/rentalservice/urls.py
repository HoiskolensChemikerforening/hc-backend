from . import views
from django.urls import path, re_path

app_name = "rentalservice"

urlpatterns = [path("", views.index, name="index"),
               re_path(r"^ny", views.new_object, name="new_object"),
               path("<int:rentalobject_id>", views.detail, name="detail")]

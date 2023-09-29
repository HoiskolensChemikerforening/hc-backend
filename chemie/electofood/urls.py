from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from . import views

app_name = "electofood"

# Events
urlpatterns = [
    path(
        "", views.index, name="index_valgomat"
    )]

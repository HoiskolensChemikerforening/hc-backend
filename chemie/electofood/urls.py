from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from . import views

app_name = "electofood"

# Events
urlpatterns = [
    path("", views.index, name="index_valgomat"),
    path("personlig/<int:id>/", views.valgomat_form, name="valgomat_form"),
    path("komitee/<int:id>/<int:committee_id>/", views.valgomat_form, name="committee_valgomat_form"),
    path("resultater/<int:id>", views.valgomat_result, name="valgomat_result"),
]

from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from . import views

app_name = "electofood"

# Events
urlpatterns = [
    path("", views.index, name="index_valgomat"),
    path("personlig/<int:id>/", views.valgomat_form, name="valgomat_form"),
    path(
        "komitee/<int:id>/<int:committee_id>/",
        views.valgomat_form,
        name="committee_valgomat_form",
    ),
    path("resultater/<int:id>", views.valgomat_result, name="valgomat_result"),
    path("opprett/", views.create_valgomat, name="valgomat_opprett"),
    path(
        "opprett/<int:id>/",
        views.create_valgomat,
        name="valgomat_opprett_edit",
    ),
    path("rediger/<int:id>/", views.edit_valgomat, name="valgomat_rediger"),
    path(
        "rediger/<int:id>/slett/<int:question_id>/",
        views.delete_question,
        name="valgomat_delete_question",
    ),
    path(
        "rediger/<int:id>/slett/valgomat/<int:valgomat_id>/",
        views.delete_valgomat,
        name="valgomat_delete",
    ),
]

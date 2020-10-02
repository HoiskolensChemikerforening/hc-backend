from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from . import views

app_name = "sugepodden"

urlpatterns = [
    path("", views.list_all, name="index"),
    path("opprett/", views.create_podcast, name="create"),
    path(
        "slett/<int:pk>/",
        views.DeletePodcastView,
        name="delete_podcast",
    ),
    path(
        "slett/",
        permission_required("sugepodden.delete_podcast")(
            views.ListPodcastDeleteView.as_view()
        ),
        name="delete_list_podcast",
    )
]

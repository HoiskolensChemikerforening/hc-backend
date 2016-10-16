from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit', views.edit, name='edit'),
    url(
        r'^user-autocomplete/',
        views.UserAutocomplete.as_view(),
        name='user-autocomplete',
    ),
]

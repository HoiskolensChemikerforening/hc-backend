from django.conf.urls import url

from . import views

app_name = 'elections'


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^vote/', views.post_votes)
]

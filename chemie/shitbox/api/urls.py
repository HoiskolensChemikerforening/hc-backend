from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

from .views import CreateView

router = routers.DefaultRouter()

router.register('submission', CreateView, base_name='submissions')

urlpatterns = [
    url(r'^', include(router.urls)),
]


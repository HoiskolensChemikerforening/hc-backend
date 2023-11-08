from . import views
from django.urls import path

app_name = "exchangepage"

urlpatterns = [path("", views.index, name="index"),
               path("<int:pk>/", views.detailViews, name="detail"),
               path("opprett/", views.createViews, name="create"),
               path("<str:city_name>/", views.cityPageViews, name="citypage")]
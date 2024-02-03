from . import views
from django.urls import path

app_name = "exchangepage"

urlpatterns = [path("", views.index, name="index"),
               path('travelletter/<int:pk>/', views.displayIndividualLetter, name='detail'),
               path("opprett/", views.createViews, name="create"),
               path("admin/", views.adminViews, name="admin"),
               path("admin/<int:pk>/", views.adminDetailViews, name="admindetail"),
               path("<str:city_name>/", views.cityPageViews, name="citypage")]
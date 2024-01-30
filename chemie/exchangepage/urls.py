from . import views
from django.urls import path

app_name = "exchangepage"

urlpatterns = [path("", views.index, name="index"),
               path("<int:pk>/", views.detailViews, name="detail"),
               path("opprett/", views.createViews, name="create"),
               path("opprettspørsmål/", views.createQuestionViews, name="createquestion"),
               path("admin/", views.adminViews, name="admin"),
               path("adminspørsmål/", views.adminQuestionViews, name="adminquestion"),
               path("adminspørsmål/<int:pk>/", views.adminQuestionDetailViews, name="adminquestiondetail"),
               path("admin/<int:pk>/", views.adminDetailViews, name="admindetail"),
               path("<str:city_name>/", views.cityPageViews, name="citypage")]
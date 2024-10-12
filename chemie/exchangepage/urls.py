from . import views
from django.urls import path

app_name = "exchangepage"

urlpatterns = [path("", views.index, name="index"),
               path('travelletter/<int:pk>/', views.displayIndividualLetter, name='detail'),
               path("opprett/", views.createTravelletterViews, name="create"),
               path("opprett/bilder/<int:pk>", views.createImageViews, name="createimage"),
               path("opprett/spørsmål/<int:pk>", views.createExperienceViews, name="createexperience"),
               path("opprettspørsmål/", views.createQuestionViews, name="createquestion"),
               path("admin/", views.adminViews, name="admin"),
               path("adminspørsmål/", views.adminQuestionViews, name="adminquestion"),
               path("adminspørsmål/<int:pk>/", views.adminQuestionDetailViews, name="adminquestiondetail"),
               path("admin/<int:pk>/", views.adminDetailViews, name="admindetail"),
               path("admin/bilder/<int:pk>/", views.adminDetailImageViews, name="admindetailimage"),
               path("admin/spørsmål/<int:pk>/", views.adminDetailExperienceViews, name="admindetailexperience"),
               path("admin/slettreisebrev/<int:pk>", views.deleteTravelletter, name="deletetravelletter"),
               path("admin/slettspørsmål/<int:pk>", views.deleteExperienceViews, name="deleteexperience"),
               path("admin/slettbilder/<int:pk>", views.deleteImages, name="deleteimages"),
               path("nedtelling/", views.countDownViews, name="countdown"),  # For countdown, can be removed afterwards
               path("<str:city_name>/", views.cityPageViews, name="citypage")]


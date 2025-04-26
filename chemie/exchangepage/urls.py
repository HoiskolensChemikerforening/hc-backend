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
               path("<str:city_name>/", views.cityPageViews, name="citypage"),
               # API
               path("api/travelletter/<int:pk>/", views.displayIndividualLetterAPI.as_view(), name="apidetail"),
               path("api/opprett/", views.createTravelletterAPI.as_view(), name="apicreate"),
               path("api/opprettspørsmål/", views.createQuestionAPI.as_view(), name="apicreatequestion"),
               path("api/admin/", views.adminAPI.as_view(), name="apiadmin"),
               path("api/adminspørsmål/", views.adminQuestionViewsAPI.as_view(), name="apiadminquestion"),
               path("api/adminspørsmål/<int:pk>/", views.adminQuestionDetailViewsAPI.as_view(), name="apiadminquestiondetail"),
               path("api/admin/<int:pk>/", views.adminDetailViewsAPI.as_view(), name="apiadmindetail"),
               path("api/admin/bilder/<int:pk>/", views.adminDetailImageViewsAPI.as_view(), name="apiadmindetailimage"),
               path("api/opprett/bilder/<int:pk>", views.createImageViewsAPI.as_view(), name="apicreateimage"),
               ]


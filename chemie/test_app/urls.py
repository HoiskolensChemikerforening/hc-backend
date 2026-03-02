from django.urls import path
from . import views

app_name = "test_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("intermediate/", views.tamegtiltestapp2, name="test_app_2_ta_meg_til_den"),
    
]

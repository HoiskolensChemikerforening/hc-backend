from django.conf.urls import url
from .views import index, refill, add_item, add_category


app_name = "shop"

urlpatterns = [
    url(r"^$", index, name="index"),
    url(r"^refill-balance", refill, name="refill"),
    url(r"^add-item/", add_item, name="add-item"),
    url(r"^add-category/", add_category, name="add-category"),
]

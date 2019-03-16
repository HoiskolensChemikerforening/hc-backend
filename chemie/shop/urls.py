from django.conf.urls import url
from .views import index, refill, add_item, add_category, remove_item, admin


app_name = "shop"

urlpatterns = [
    url(r"^$", index, name="index"),
    url(r"^admin/", admin, name="admin"),
    url(r"^refill-balance", refill, name="refill"),
    url(r"^add-item/", add_item, name="add-item"),
    url(r"^add-category/", add_category, name="add-category"),
    url(r"^remove-item/(?P<pk>[0-9]+)", remove_item, name="remove-item")
]

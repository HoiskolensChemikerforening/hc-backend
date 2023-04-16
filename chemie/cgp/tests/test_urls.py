from django.test import SimpleTestCase

from django.urls import reverse, resolve
from ..views import index
from ..views_admin import cgp_admin, DeleteView


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        """
        gets viewfunction by url and compares it with the viewfunction expected
        """
        url = reverse("cgp:index")
        self.assertEqual(resolve(url).func, index)

    def test_cgp_admin_url_is_resolved(self):
        url = reverse("cgp:cgp_admin")
        self.assertEqual(resolve(url).func, cgp_admin)

    def test_cgp_country_delete_url_is_resolved(self):
        url = reverse("cgp:country_delete", args=[1])
        self.assertEqual(resolve(url).func.view_class, DeleteView)


"""

path("admin/", views_admin.cgp_admin, name="cgp_admin"),
    path("admin/<int:cgp_id>/", views_admin.cgp_edit, name="cgp_edit"),
    path("admin/<int:cgp_id>/group/add/", views_admin.group_add, name="group_add"),
    path("admin/<int:cgp_id>/group/<int:group_id>/", views_admin.group_edit, name="group_edit"),
    path("admin/<int:cgp_id>/group/<int:group_id>/delete/", views_admin.DeleteView.as_view(
            key="group_id", objecttype=Group, redirect_url="cgp_edit"), name="group_delete"
        ),
    path("admin/country/add/", views_admin.country_add, name="country_add"),
    path("admin/country/<int:country_id>/", views_admin.country_edit, name="country_edit"),
    path("admin/country/<int:country_id>/delete/", views_admin.DeleteView.as_view(
        key="country_id", objecttype=Country, redirect_url="cgp_admin"), name="country_delete"
         ),
    path("<slug:slug>/", views.vote_index, name="vote_index"),
    path("api", views.CGPListViewTemplate.as_view(), name="cgpapi"),
"""

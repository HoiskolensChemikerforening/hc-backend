from django.test import SimpleTestCase

from django.urls import reverse, resolve
from ..views import index, vote_index, CGPListViewTemplate
from ..views_admin import cgp_admin, DeleteView, cgp_edit, group_add, group_edit, country_add, country_edit


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

    def test_cgp_edit_url_is_resolved(self):
        url = reverse("cgp:cgp_edit", args=[1])
        self.assertEqual(resolve(url).func, cgp_edit)

    def test_group_add_url_is_resolved(self):
        url = reverse("cgp:group_add", args=[1])
        self.assertEqual(resolve(url).func, group_add)

    def test_group_edit_url_is_resolved(self):
        url = reverse("cgp:group_edit", args=[1, 1])
        self.assertEqual(resolve(url).func, group_edit)

    def test_country_add_url_is_resolved(self):
        url = reverse("cgp:country_add")
        self.assertEqual(resolve(url).func, country_add)

    def test_country_edit_url_is_resolved(self):
        url = reverse("cgp:country_edit", args=[1])
        self.assertEqual(resolve(url).func, country_edit)

    def test_vote_index_url_is_resolved(self):
        url = reverse("cgp:vote_index", args=["cytosolkysten"])
        self.assertEqual(resolve(url).func, vote_index)

    def test_group_delete_url_is_resolved(self):
        url = reverse("cgp:group_delete", args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, DeleteView)

    def test_cgpapi_url_is_resolved(self):
        url = reverse("cgp:cgpapi")
        self.assertEqual(resolve(url).func.view_class, CGPListViewTemplate)



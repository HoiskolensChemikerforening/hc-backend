from django.test import TestCase
from .models import Specialization, Company, Interview


class CompanyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Company.objects.create(name='first company name')
        Company.objects.create(description='filler description here')

    def test_title_content(self):
        company = Company.objects.get(id=1)
        expected_object_name = f'{company.name}'
        self.assertEquals(expected_object_name, 'first company name')

    def test_description_content(self):
        company = Company.objects.get(id=2)
        expected_object_name = f'{company.description}'
        self.assertEquals(expected_object_name, 'filler description here')


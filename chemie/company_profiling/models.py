from django.db import models
from multiselectfield import MultiSelectField
from extended_choices import Choices


FIELD_OF_STUDY = (('prosess', 'Prosessteknologi'),
                  ('biotek', 'Bioteknologi'),
                  ('mattek', 'Materialteknologi'),
                  ('kjemi', 'Kjemi'))


class Company(models.Model):
    # Company name
    name = models.CharField(max_length=None, verbose_name="Navn")

    # Company logo
    logo = models.ImageField(upload_to='company_profiling', verbose_name="Logo")

    # Which fields of study the company is relevant for
    field_of_study = MultiSelectField(choices=FIELD_OF_STUDY)

    # Short company description
    description = models.TextField(verbose_name="Beskrivelse")


class Interview(models.Model):
    # Name of the person
    name = models.CharField(max_length=None, verbose_name="Navn")

    # Company
    company = models.ForeignKey(Company)

    # Name of the position the person holds at the company
    position = models.CharField(max_length=None, verbose_name="Arbeidsstilling")

    # Image of the interviewee
    image = models.ImageField(upload_to='company_profiling', verbose_name="Bilde")

    # The interview itself
    interview = models.TextField(verbose_name="Intervju")

    # The field of study the person went through
    field_of_study = Choices(choices=FIELD_OF_STUDY)

    def __str__(self):
        return self.name + ", " + self.position + " for " + self.company.name

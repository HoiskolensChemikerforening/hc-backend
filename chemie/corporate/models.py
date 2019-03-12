from django.db import models

class Interview(models.Model):
    corporate = models.ForeignKey()
    person = models.CharField(max_length=40)
    text = models.RichTextField(
        verbose_name="Intervju"
    )
    picture = models.ImageField()






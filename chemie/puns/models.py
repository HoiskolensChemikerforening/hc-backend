from django.db import models
from django.contrib.auth.models import User


class Submission(models.Model):
    content = models.TextField(max_length=3000, verbose_name="Vits")
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, verbose_name="Innsender", on_delete=models.CASCADE
    )
    used = models.BooleanField(
        default=False
    )  # For Webkom to keep track on used submissions

from django.db import models
from django.contrib.auth.models import User

class MagicAnswer(models.Model):
    VIBE_CHOICES = [
        ("positiv", "Positiv"),
        ("negativ", "Negativ"),
        ("usikker", "Usikker"),
        ("morsom", "Morsom"),
    ]
    tekst = models.CharField(max_length = 200)
    vibe = models.CharField(max_length = 20, choices=VIBE_CHOICES, default="usikker")

    def __str__(self):
        return f"{self.tekst} ({self.vibe})"
from django.db import models


class Event(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField(default=None, blank=True)
    event_name = models.CharField(max_length=120)

    def __str__(self):
        return self.event_name

from django.contrib import admin

from .models import Candidate, Position

admin.site.register(Candidate)
admin.site.register(Position)

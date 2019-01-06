from django.contrib import admin

from .models import Candidate, Position, Election

admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(Election)

from django.contrib import admin

from .models import Candidates, Position, Election

admin.site.register(Candidates)
admin.site.register(Position)
admin.site.register(Election)


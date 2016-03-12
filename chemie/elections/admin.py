from django.contrib import admin

from .models import Candidate, Position, Election, Ticket

admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(Election)
admin.site.register(Ticket)

from django.contrib import admin
from .models import Event, EventRegistration, RegistrationMessage#, CompanyEvent


@admin.register(EventRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ('status',)

admin.site.register(RegistrationMessage)
admin.site.register(Event)
#admin.site.register(CompanyEvent)

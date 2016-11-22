from django.contrib import admin
from .models import Event, Registration, RegistrationMessage, CompanyEvent

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ('status',)

admin.site.register(RegistrationMessage)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(CompanyEvent)
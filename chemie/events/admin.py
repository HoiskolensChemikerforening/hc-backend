from django.contrib import admin
from .models import Event, BaseRegistration, RegistrationMessage, CompanyEvent

@admin.register(BaseRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ('status',)

admin.site.register(RegistrationMessage)
admin.site.register(Event)
admin.site.register(CompanyEvent)
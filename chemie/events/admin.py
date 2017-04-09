from django.contrib import admin
from .models import Event, EventRegistration, RegistrationMessage#, CompanyEvent
from django.contrib.admin.filters import AllValuesFieldListFilter, RelatedFieldListFilter, ChoicesFieldListFilter


class DropdownFilter(RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'


@admin.register(EventRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ('status', 'payment_status', ('event', DropdownFilter))
    ordering = ('-created',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_display = ('event', 'user', 'created', 'edited', 'payment_status', 'companion')


admin.site.register(RegistrationMessage)
admin.site.register(Event)
#admin.site.register(CompanyEvent)

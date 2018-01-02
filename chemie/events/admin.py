from django.contrib import admin
from .models import Social, EventRegistration, RegistrationMessage, Bedpres, BedpresRegistration
from django.contrib.admin.filters import AllValuesFieldListFilter, RelatedFieldListFilter, ChoicesFieldListFilter


class DropdownFilter(RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'


@admin.register(EventRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ('status', 'payment_status', ('event', DropdownFilter))
    ordering = ('-created',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_display = ('event', 'user', 'created', 'edited', 'payment_status', 'companion',)


@admin.register(BedpresRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ('status', ('event', DropdownFilter))
    ordering = ('-created',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_display = ('event', 'user', 'created', 'edited')


@admin.register(Social)
class EventAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    ordering = ('-date',)
    search_fields = ('title',)
    list_display = ('title', 'sluts', 'date', 'created', 'edited',
                    'companion', 'sleepover', 'night_snack', 'published')


@admin.register(Bedpres)
class EventAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    ordering = ('-date',)
    search_fields = ('title',)
    list_display = ('title', 'sluts', 'date', 'created', 'edited', 'published')


#admin.site.register(RegistrationMessage)


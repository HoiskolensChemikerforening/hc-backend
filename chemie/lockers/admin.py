from django.contrib import admin

from .models import Locker, LockerUser, Ownership


# https://stackoverflow.com/a/43200689
class ReferrerFilter(admin.SimpleListFilter):
    title = 'is taken'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'owner__isnull'

    def lookups(self, request, model_admin):
        return (
            ('False', 'is taken'),
            ('True', 'is free'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'False':
            return queryset.filter(owner__isnull=False)
        if self.value() == 'True':
            return queryset.filter(owner__isnull=True)


class LockerAdmin(admin.ModelAdmin):
    search_fields = ['number', 'owner__user__first_name', 'owner__user__last_name', ]
    list_display = ['number', 'owner', 'get_is_active']
    list_filter = (ReferrerFilter, 'owner__is_active', 'owner__is_confirmed')

    # https://www.darklaunch.com/2015/02/04/how-to-prefetch-related-queryset-in-django-admin
    def get_queryset(self, request):
        my_model = super(LockerAdmin, self).get_queryset(request)
        my_model = my_model.prefetch_related('owner', 'owner__user')
        return my_model

    def get_is_active(self, obj):
        return obj.owner.is_active if obj.owner else None

    class Meta:
        model = Locker
        ordering = ['number']


class LockerUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'created']
    list_filter = ['created']
    search_fields = ['email', 'first_name', 'last_name']
    list_display_links = None

    class Meta:
        model = LockerUser


class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['get_locker_number', 'get_user', 'created', 'edited', 'is_active', 'is_confirmed']
    list_filter = ('is_active', 'is_confirmed', 'created', 'edited',)
    search_fields = ['locker__number', 'user__first_name', 'user__last_name', 'user__email']

    def get_user(self, obj):
        return obj.user.email

    get_user.short_description = 'User'
    get_user.admin_order_field = 'locker__email'

    def get_locker_number(self, obj):
        return obj.locker.number

    get_locker_number.short_description = 'skapnummer'
    get_locker_number.admin_order_field = 'number'

    # https://www.darklaunch.com/2015/02/04/how-to-prefetch-related-queryset-in-django-admin
    def get_queryset(self, request):
        my_model = super(OwnershipAdmin, self).get_queryset(request)
        my_model = my_model.prefetch_related('locker', 'user')
        return my_model

    class Meta:
        model = Ownership


admin.site.register(Locker, LockerAdmin)
admin.site.register(LockerUser, LockerUserAdmin)
admin.site.register(Ownership, OwnershipAdmin)

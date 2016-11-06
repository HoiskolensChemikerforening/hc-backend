from django.contrib import admin

from .models import Locker, LockerUser, Ownership, LockerConfirmation


class LockerAdmin(admin.ModelAdmin):
    search_fields = ["number"]

    # list_display_links = None

    class Meta:
        model = Locker
        ordering = ['number']


class LockerUserAdmin(admin.ModelAdmin):
    list_display = ["username"]
    list_filter = ["created"]
    search_fields = ["username"]
    list_display_links = None

    class Meta:
        model = LockerUser


class OwnershipAdmin(admin.ModelAdmin):
    list_display = ["get_locker_number", "get_user"]

    def get_user(self, obj):
        return obj.user.username

    get_user.short_description = 'User'
    get_user.admin_order_field = 'locker__username'

    def get_locker_number(self, obj):
        return obj.locker.number

    get_locker_number.short_description = "skapnummer"
    get_locker_number.admin_order_field = "number"

    class Meta:
        model = Ownership


class ConfirmationAdmin(admin.ModelAdmin):

    class Meta:
        model = LockerConfirmation


admin.site.register(LockerConfirmation, ConfirmationAdmin)
admin.site.register(Locker, LockerAdmin)
admin.site.register(LockerUser, LockerUserAdmin)
admin.site.register(Ownership, OwnershipAdmin)

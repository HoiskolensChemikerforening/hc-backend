from django.contrib import admin
from .models import Locker, LockerUser, Ownership

admin.site.register(Locker)


class LockerUserAdmin(admin.ModelAdmin):
    list_display = ["username", "internal_user"]
    list_filter = ["created"]
    search_fields = ["username", "internal_user__username"]
    list_display_links = None
    
    class Meta:
        model = LockerUser


class OwnershipAdmin(admin.ModelAdmin):
    list_display = ["get_locker_number", "get_user"]

    def get_user(self, obj):
        if obj.user.username:
            return obj.user.username
        else:
            return obj.user.internal_user.username

    get_user.short_description = 'User'
    get_user.admin_order_field = 'locker__username'

    def get_locker_number(self, obj):
        return(obj.locker.number)

    get_locker_number.short_description = "number"
    get_locker_number.admin_order_field = "Skapnummer"

    class Meta:
        model = Ownership


admin.site.register(LockerUser, LockerUserAdmin)
admin.site.register(Ownership, OwnershipAdmin)

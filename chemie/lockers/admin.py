from django.contrib import admin
from .models import Locker, LockerUser, Ownership

admin.site.register(Locker)

admin.site.register(Ownership)

class LockerUserAdmin(admin.ModelAdmin):
    list_display = ["username", "internal_user"]
    list_filter = ["created"]
    search_fields = ["username", "internal_user__username"]
    list_display_links = None
    class Meta:
      model = LockerUser


admin.site.register(LockerUser, LockerUserAdmin)

from django.contrib import admin
from .models import Locker, LockerUser, Ownership

admin.site.register(Locker)
admin.site.register(LockerUser)
admin.site.register(Ownership)

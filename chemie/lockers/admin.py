from django.contrib import admin
from .models import Locker, User, Ownership

admin.site.register(Locker)
admin.site.register(User)
admin.site.register(Ownership)
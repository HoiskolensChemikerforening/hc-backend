from django.contrib import admin

from .models import FundsApplication, OfficeApplication

admin.site.register(FundsApplication)
admin.site.register(OfficeApplication)
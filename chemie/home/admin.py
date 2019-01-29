from django.contrib import admin

from .models import FundsApplication, OfficeApplication

admin.site.register(FundsApplication)

@admin.register(OfficeApplication)
class OfficeApplication(admin.ModelAdmin):
    ordering = ('-created',)
    list_display = ('author', 'student_username', 'created')
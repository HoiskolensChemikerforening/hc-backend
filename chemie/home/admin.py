from django.contrib import admin

from .models import FundsApplication, OfficeApplication, RefundApplication, RefundItem

admin.site.register(FundsApplication)
admin.site.register(RefundApplication)
admin.site.register(RefundItem)


@admin.register(OfficeApplication)
class OfficeApplication(admin.ModelAdmin):
    ordering = ("-created",)
    list_display = ("author", "student_username", "created")

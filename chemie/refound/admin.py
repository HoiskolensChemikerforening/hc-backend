from .models import RefoundRequest, Refound
from django.contrib import admin

@admin.register(RefoundRequest)
class CommitteeAdmin(admin.ModelAdmin):
    ordering = ("created",)
    list_display = ("created", "user")

@admin.register(Refound)
class CommitteeAdmin(admin.ModelAdmin):
    ordering = ("date",)
    list_display = ("date", "store","event","price")


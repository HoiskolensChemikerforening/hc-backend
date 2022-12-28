from django.contrib import admin

from .models import CGP

admin.site.site_title = "CGP"


@admin.register(CGP)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ["is_open"]

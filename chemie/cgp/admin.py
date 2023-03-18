from django.contrib import admin

from .models import CGP, Country, CgpPosition, Group, Vote

admin.site.site_title = "CGP"


@admin.register(CGP)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ["is_open"]

@admin.register(Country)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ["country_name"]

@admin.register(CgpPosition)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ["group"]

@admin.register(Group)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ["real_name"]

@admin.register(Vote)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ["group"]


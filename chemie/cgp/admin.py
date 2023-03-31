from django.contrib import admin
from .models import CGP, Country, Group, Vote

admin.site.site_title = "CGP"


@admin.register(CGP)
class CGPAdmin(admin.ModelAdmin):
    list_display = ["year"]

@admin.register(Country)
class CGPAdmin(admin.ModelAdmin):
    list_display = ["country_name"]

@admin.register(Group)
class CGPAdmin(admin.ModelAdmin):
    list_display = ["real_name", "country", "song_name"]

@admin.register(Vote)
class CGPAdmin(admin.ModelAdmin):
    list_display = ["group", "user", "final_vote"]


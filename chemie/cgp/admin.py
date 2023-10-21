from django.contrib import admin
from .models import CGP, Country, Group, Vote

admin.site.site_title = "CGP"


@admin.register(CGP)
class CGPAdmin(admin.ModelAdmin):
    """
    Register CGP model to admin.
    Displayed fields in list: year
    """

    list_display = ["year"]


@admin.register(Country)
class CGPAdmin(admin.ModelAdmin):
    """
    Register Country model to admin.
    Displayed fields in list: country_name
    """

    list_display = ["country_name"]


@admin.register(Group)
class CGPAdmin(admin.ModelAdmin):
    """
    Register Group model to admin.
    Displayed fields in list: real_name, country, song_name
    """

    list_display = ["real_name", "country", "song_name"]


@admin.register(Vote)
class CGPAdmin(admin.ModelAdmin):
    """
    Register Group model to admin.
    Displayed fields in list: group, user, final_vote
    """

    list_display = ["group", "user", "final_vote"]

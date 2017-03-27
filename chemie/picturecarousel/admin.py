from django.contrib import admin

# Register your models here.
from .models import Picture

class PostAdmin(admin.ModelAdmin):
    list_display = ["description", "author", "date", "approved"]
    list_filter = ["date"]
    search_fields = ["description", "author__username", "approved"]
    list_display_links = None
    class Meta:
        model = Picture



admin.site.register(Picture, PostAdmin)

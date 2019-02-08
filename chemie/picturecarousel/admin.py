from django.contrib import admin

# Register your models here.
from .models import Contribution


class PostAdmin(admin.ModelAdmin):
    list_display = ["author", "date", "approved"]
    list_filter = ["date"]
    search_fields = ["description", "author__username", "approved"]
    list_display_links = None

    class Meta:
        model = Contribution


admin.site.register(Contribution, PostAdmin)

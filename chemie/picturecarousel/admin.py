from django.contrib import admin

# Register your models here.
from .models import Submission

class PostAdmin(admin.ModelAdmin):
    list_display = ["author", "date", "approved"]
    list_filter = ["date"]
    search_fields = ["description", "author__username", "approved"]
    list_display_links = None
    class Meta:
        model = Submission



admin.site.register(Submission, PostAdmin)

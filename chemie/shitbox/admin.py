from django.contrib import admin

# Register your models here.
from .models import Submission

class PostAdmin(admin.ModelAdmin):
    list_display = ["content", "author", "date"]
    list_filter = ["date"]
    search_fields = ["content", "author__username"]
    list_display_links = None
    class Meta:
        model = Submission



admin.site.register(Submission, PostAdmin)

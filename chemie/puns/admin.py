from django.contrib import admin
from .models import Puns_Submission


class PostAdmin(admin.ModelAdmin):
    list_display = ["content", "author", "date", "accepted"]
    list_filter = ["date"]
    search_fields = ["content", "author__username"]
    list_display_links = None

    class Meta:
        model = Puns_Submission


admin.site.register(Puns_Submission, PostAdmin)

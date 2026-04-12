from django.contrib import admin
from .models import MagicAnswer

class MagicAnswerAdmin(admin.ModelAdmin):
    list_display = ("tekst", "vibe")

admin.site.register(MagicAnswer, MagicAnswerAdmin)
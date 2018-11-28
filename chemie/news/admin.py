from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('published_date',)
    ordering = ('-published_date',)
    search_fields = ('title',)
    list_display = ('title', 'published_date',)


#admin.site.register(Article)
list_display = ('title', 'published_date', 'published')
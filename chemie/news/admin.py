from django.contrib import admin
from .models import Article, ArticleComment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('published_date',)
    ordering = ('-published_date',)
    search_fields = ('title',)
    list_display = ('title', 'published_date',)


@admin.register(ArticleComment)
class ArticleComment(admin.ModelAdmin):
    list_filter = ('published_date',)
    ordering = ('-published_date',)
    search_fields = ('article',)
    list_display = ('article', 'author', 'text',)

#admin.site.register(Article)
#admin.site.register(ArticleComment)

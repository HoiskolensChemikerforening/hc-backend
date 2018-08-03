from django.contrib import admin

# Register your models here.
from .models import Item, Category


class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    list_filter = ["name", "price"]
    search_fields = ["name"]

    class Meta:
        model = Item


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Category


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
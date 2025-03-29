from django.contrib import admin
from .models import Ingredients, Recipes, Kategori


# Register your models here.


admin.site.register(Recipes)
admin.site.register(Ingredients)
admin.site.register(Kategori)

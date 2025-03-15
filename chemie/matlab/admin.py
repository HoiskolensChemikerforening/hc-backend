from django.contrib import admin
from .models import Ingredients, Recipes


# Register your models here.


admin.site.register(Recipes)
admin.site.register(Ingredients)

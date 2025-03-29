from django.contrib import admin
from .models import Ingredients, Recipes
from .forms import RecipesForm

# Register your models here.
admin.site.register(Recipes)
admin.site.register(Ingredients)
from django.contrib import admin
from .models import Recipes
from .forms import RecipesForm

# Register your models here.
admin.site.register(Recipes)

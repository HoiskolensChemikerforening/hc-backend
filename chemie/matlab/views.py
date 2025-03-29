from django.shortcuts import render
from .models import Recipes, Ingredients
from .forms import RecipesForm
from django.contrib import messages


def index(request):
    a = Recipes.objects.all()
    b = Ingredients.objects.all()


    context = {"Recipes": a, "Ingredients": b}


    return render(request, "index.html", context)


def createRecipes(request):
    form = RecipesForm()
    print(0)
    if request.method == "POST":
        form = RecipesForm(data = request.POST)
        print(1)
        print(form)
        print("#"*40)
        print(request.POST)
        print("#"*40)
        print(form.errors)

        if form.is_valid():
            print(2)
            form_instace = form.save(commit=False)
            form_instace.save()
            form.save_m2m()
            messages.add_message(
                request,
                messages.SUCCESS,
                "MatOppskrift er lagret",
            )

    context = {"lageoppskrift":form}
    return render(request, "lageoppskrift.html", context) #sjekke etterpå
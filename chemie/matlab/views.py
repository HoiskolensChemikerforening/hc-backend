from django.shortcuts import render
from .models import Recipes
from .forms import RecipesForm
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required

@login_required
def index(request):
    a = Recipes.objects.all()
    


    context = {"Recipes": a,}


    return render(request, "index.html", context)

@login_required
def createRecipes(request):
    form = RecipesForm()
    print(0)
    if request.method == "POST":
        form = RecipesForm(request.POST, request.FILES)
        print(1)
        print(form)
        print("#"*40)
        print(request.POST)
        print("#"*40)
        print(form.errors)

        if form.is_valid():
            print(format)
            print(2)
            form_instace = form.save(commit=False)
            form_instace.author = request.user
            form_instace.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "MatOppskrift er lagret",
            )

    context = {"lageoppskrift":form}
    return render(request, "lageoppskrift.html", context) #sjekke etterpå
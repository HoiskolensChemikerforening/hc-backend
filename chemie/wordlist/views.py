
from .models import Word
from .models import Category
from .forms import WordInput, CategoryInput
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic.list import ListView
from chemie.customprofile.models import Profile
from django.contrib.auth.decorators import login_required

@login_required()
def ordListe(request):
    # print(request.user)
    profile = get_object_or_404(Profile, user=request.user)
    # print(profile.grade)
    if int(profile.grade) < 2:
       alle_ord = Word.objects.all().filter(secret=False)

    else:
       alle_ord = Word.objects.all()

    # alle_ord = Word.objects.all()

    context = {"ord": alle_ord}


    return render(request, "wordall.html", context)



@login_required()
def createWord(request):
    if request.method == "POST":
        wordform = WordInput(request.POST)
        if wordform.is_valid():
            wordform.save()


    else:
        wordform = WordInput()

    context = {"wordform":wordform}
    return render(request, "createWord.html", context)

@login_required()
def adminWord(request):
    context = {}
    return render(request, "adminWord.html", context)


def category(request):

    alle_ord = Category.objects.all()
    context = {"ord": alle_ord}
    return render(request, "category.html", context)


def details(request, pk):
    
    alle_ord = Category.objects.all()
    context = {"ord": alle_ord}
    return render(request, "details.html", context)

def admincategoryViews(request):
    categories = Category.objects.all()
    context = {"admincategory":categories}
    return render(request, "admincategory.html", context)

def editcategoryViews(request, pk):
    category = get_object_or_404(Category, id = pk)

    
    if request.method == "POST":
        categoryform = CategoryInput(request.POST,instance=category)
        if categoryform.is_valid():
            category_instance = categoryform.save(commit=False)
            category_instance.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                "OG FET B)",
                extra_tags="KATEGORIEN DIN ER LAGRET"
            )
            return HttpResponseRedirect(reverse("Wordlist:admincategory"))
    else:
        categoryform = CategoryInput(instance=category)
    context = {"categoryform":categoryform, "category":category}
    return render(request, "editcategory.html", context )

@login_required
def createcategoryViews(request):
    if request.method == "POST":
        categoryform = CategoryInput(request.POST)

        if categoryform.is_valid():
            category_instance = categoryform.save(commit=False)
            category_instance.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                "OG FET B)",
                extra_tags="KATEGORIEN DIN ER LAGRET"
            )
            return HttpResponseRedirect(reverse("wordlist:admincategory"))
        
    else:
        categoryform = CategoryInput()
    context = {"categoryform":categoryform}
    return render(request, "createcategory.html", context )



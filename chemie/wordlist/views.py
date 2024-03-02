
from .models import Word
from .models import Category
from .forms import WordInput
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
       all_words = Word.objects.all().filter(secret=False).order_by("word")
       

    else:
       all_words = Word.objects.all()

    

    context = {"words": all_words}
    


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
def categoryViews(request):
    context = {}
    return render(request, "admincategory.html", context)


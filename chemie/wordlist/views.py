
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

    
    for i in all_words:
        i.explanations = i.explanations[:25] + "..."
    
    print(all_words[0].picture)

    context = {"words": all_words}
    
    return render(request, "wordall.html", context)



@login_required()
def createWord(request):
    if request.method == "POST":
        wordform = WordInput(request.POST)
        if wordform.is_valid():
            wordform_instace = wordform.save(commit=False)
            wordform_instace.author = request.user
            wordform_instace.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Ditt ord er lagret.",
                extra_tags="Big slay",
            )
            #return redirect("refund:myrefunds")
    else:
        wordform = WordInput()
    print(request.POST)
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


def sortingMainPageView(request):
    if request.method == "POST":
    

    else:

    return render(request, "category.html")
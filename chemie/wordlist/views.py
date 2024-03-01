
from .models import Word
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
       alle_ord = Word.objects.all().filter(secret=False)

    else:
       alle_ord = Word.objects.all()

    # alle_ord = Word.objects.all()

    context = {"ord": alle_ord}


    return render(request, "wordall.html", context)



@login_required()
def CreateWord(request):
    if request.method == "POST":
        wordform = WordInput(request.POST)
        if wordform.is_valid():
            wordform.save()


    else:
        wordform = WordInput()

    context = {"wordform":wordform}
    return render(request, "createWord.html", context)


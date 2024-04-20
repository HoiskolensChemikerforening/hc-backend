
from .models import Word, Category
from .forms import WordInput, WordSearchMainPage, CategorySortingMainPage, CategoryInput
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic.list import ListView
from chemie.customprofile.models import Profile, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required()
def ordListe(request):

    alle_ord = Word.objects.all()
    form = WordSearchMainPage()
    kategorier = Category.objects.all()
    category_form = CategorySortingMainPage()
    


    if not alle_ord.exists():
        return render(request, "404.html")
    else:
        form = WordSearchMainPage(request.POST or None)

        if request.method == "POST":
            if form.is_valid():                
                if request.POST["submit"] == "Søk!":
                    the_word = form.cleaned_data.get("the_word")
                    alle_ord = Word.objects.filter(word__icontains = the_word)
                    
    if not kategorier.exists():
            return render(request, "404.html")
    else:
        category_form = CategorySortingMainPage(request.POST or None)
        if request.method == "POST":
            if category_form.is_valid():              
                if request.POST["submit"] == "Ta meg til kategorien":
                    
                    the_category = category_form.cleaned_data.get("category")
                    alle_ord = Word.objects.filter(category = the_category)
                    
                    
    for i in alle_ord:
        i.explanations = i.explanations[:25] + "..."
    


    obj_per_page = 30  # Show 25 contacts per page.
    if len(alle_ord) < obj_per_page:
        context = {"word": alle_ord, "form": form, "category": kategorier, "category_form": category_form}

    else:
        paginator = Paginator(alle_ord, obj_per_page)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        alle_ord = page_obj

    # print(request.user)
    # print(User.date_joined)
    profile = get_object_or_404(Profile, user=request.user)
    # print(profile.grade)
    # if Profile.user.date_joined
    if int(profile.grade) < 2:
       alle_ord = alle_ord.filter(secret=False).order_by("word")
    
    context = {"word": alle_ord, "form": form, "category": kategorier, "category_form": category_form}
    return render(request, "wordall.html", context)



@permission_required("wordlist.add_word")
def createWord(request):
    if request.method == "POST":
        wordform = WordInput(request.POST)
        if "nytt" in request.POST and wordform.is_valid():
            wordform_instace = wordform.save(commit=False)
            wordform_instace.author = request.user
            wordform_instace.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Ditt ord er lagret",
                extra_tags="Big slay",
            )
            return HttpResponseRedirect(reverse("wordlist:innsending"))
        
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
            return HttpResponseRedirect(reverse("wordlist:index"))
    else:
        wordform = WordInput()
    context = {"wordform":wordform}
    return render(request, "createWord.html", context)

@permission_required("wordlist.change_word")
def adminWord(request, pk):
    word = get_object_or_404(Word, id=pk)
    form = WordInput(
        request.POST or None, request.FILES or None, instance=word
    )
    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                "Ordet ble endret",
                extra_tags="Endret",
            )
            return HttpResponseRedirect(reverse("wordlist:details", args=[pk]))
    context = {"wordform": form, "word":word}
    return render(request, "createWord.html", context)

@permission_required("wordlist.delete_word")
def word_delete(request, pk):
    word = get_object_or_404(Word, id=pk)

    word.delete()
    messages.add_message(
        request, messages.SUCCESS, "Ordet ble slettet", extra_tags="Slettet"
    )
    return HttpResponseRedirect(reverse("wordlist:index"))

@login_required()
def details(request, pk):
    ordet = get_object_or_404(Word, id=pk)
    context = {"ord": ordet}
    return render(request, "details.html", context)

@permission_required("wordlist.add_word")
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


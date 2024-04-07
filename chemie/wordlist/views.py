
from .models import Word, Category
from .forms import WordInput, WordSearchMainPage, CategorySortingMainPage
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic.list import ListView
from chemie.customprofile.models import Profile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required()
def ordListe(request):

    alle_ord = Word.objects.all()
    form = WordSearchMainPage()
    kategorier = Category.objects.all()
    category_form = CategorySortingMainPage()
    


    if not alle_ord.exists():
        return render(request, "empty_word.html")
    else:
        form = WordSearchMainPage(request.POST or None)

        if request.method == "POST":
            if form.is_valid():                
                if request.POST["submit"] == "Søk!":
                    the_word = form.cleaned_data.get("the_word")
                    alle_ord = Word.objects.filter(word__icontains = the_word)
                    
    if not kategorier.exists():
            return render(request, "empty_category.html")
    else:
        category_form = CategorySortingMainPage(request.POST or None)

        if request.method == "POST":
            if category_form.is_valid():                
                if request.POST["submit"] == "Ta meg til kategorien":
                    the_category = category_form.cleaned_data.get("category")
                    context = {"the_category": the_category}
                    return render(request, "category.html", context)
                    
                    
                        



        # obj_per_page = 25  # Show 25 contacts per page.
        # if len(alle_ord) < obj_per_page:
        #     context = {"word": alle_ord, "form": form}
        # else:
        #     paginator = Paginator(alle_ord, obj_per_page)

        #     page_number = request.GET.get("page")
        #     page_obj = paginator.get_page(page_number)
        #     alle_ord = page_obj


        
    for i in alle_ord:
        i.explanations = i.explanations[:25] + "..."
    
    # print(alle_ord[0].picture)



    # # print(request.user)
    # profile = get_object_or_404(Profile, user=request.user)
    # # print(profile.grade)
    # if int(profile.grade) < 2:
    #    alle_ord = alle_ord.filter(secret=False).order_by("word")


    
    
    context = {"word": alle_ord, "form": form, "category": kategorier, "category_form": category_form}
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
    # alle_ord = Word.objects.all()
    # form = CategorySortingMainPage()
    # kategorier = Category.objects.all()


    # if not alle_ord.exists():
    #     return render(request, "empty_word.html")
    # else:

    #     if request.method == "POST":
    #         form = CategorySortingMainPage(request.POST)
    #         if form.is_valid():
    #             if request.POST["submit"] == "Sorter!":
    #                 alle_ord = Category.objects.filter(
    #                     typeOfWord=form.cleaned_data["typeOfWord"]
    #                 )
    # obj_per_page = 25  # Show 25 contacts per page.
    # if len(alle_ord) < obj_per_page:
    #     context = {"word": alle_ord, "form": form}
    # else:
    #     paginator = Paginator(alle_ord, obj_per_page)

    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #     alle_ord = page_obj

    
    # context = {"ord": alle_ord, "form": form, "category": kategorier}

    return render(request, "category.html")





def details(request, pk):
    alle_ord = Category.objects.all()
    context = {"ord": alle_ord}
    return render(request, "details.html", context)


def categoryViews(request):
    context = {}
    return render(request, "admincategory.html", context)


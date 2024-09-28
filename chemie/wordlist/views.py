
from .models import Word, Category, Noun, Verb, Adjective
from .forms import WordInput, WordSearchMainPage, CategorySortingMainPage, CategoryInput, NounInput, VerbInput, AdjectiveInput, CheckWhatFormForm
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
                    

    profile = get_object_or_404(Profile, user=request.user)

    if int(profile.grade) < 2:
       alle_ord = alle_ord.filter(secret=False).order_by("word")


    obj_per_page = 30  # Show 30 words per page.
    if len(alle_ord) < obj_per_page:
        context = {"word": alle_ord, "form": form, "category": kategorier, "category_form": category_form}

    else:
        paginator = Paginator(alle_ord, obj_per_page)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        alle_ord = page_obj
  

    for i in alle_ord:
        i.explanations = i.explanations[:25] + "..."
    
    context = {"word": alle_ord, "form": form, "category": kategorier, "category_form": category_form}
    return render(request, "wordall.html", context)


# There may occur a lot of duplicate Nouns, Verbs or Adjectives: (unique = False).
# That is because it is needed to make the forms valid in createWord and adminWord. 
# They will not be valid if you make changes and the variable aleady exists.


@permission_required("wordlist.add_word")
def createWord(request):
    

    if request.method == "POST" and checkwhatformform.is_valid():
        if checkwhatformform == "Et annet type ord":
            wordform = WordInput()
        if checkwhatformform == "Verb":
            verbform = VerbInput()
        if checkwhatformform == "Substantiv":
            nounform = NounInput()
        if checkwhatformform == "Adjektiv":
            adjectiveform = AdjectiveInput()


    if request.method == "POST":
        wordform = WordInput(data=request.POST, files=request.FILES)
        nounform = NounInput(data=request.POST, files=request.FILES)
        verbform = VerbInput(data=request.POST, files=request.FILES)
        adjectiveform = AdjectiveInput(data=request.POST, files=request.FILES)
        
        if "nytt" in request.POST and nounform.is_valid():       
            nounform_instace = nounform.save(commit=False)
            nounform_instace.author = request.user
            nounform_instace.save()
            nounform.save_m2m()

        if "nytt" in request.POST and verbform.is_valid():       
            verbform_instace = verbform.save(commit=False)
            verbform_instace.author = request.user
            verbform_instace.save()
            verbform.save_m2m()

        if "nytt" in request.POST and adjectiveform.is_valid():       
            adjectiveform_instace = adjectiveform.save(commit=False)
            adjectiveform_instace.author = request.user
            adjectiveform_instace.save()
            adjectiveform.save_m2m()


        if "nytt" in request.POST and wordform.is_valid():
            wordform_instace = wordform.save(commit=False)
            wordform_instace.author = request.user
            wordform_instace.save()
            wordform.save_m2m()

                
            messages.add_message(
                request,
                messages.SUCCESS,
                "Ditt ord er lagret",
                extra_tags="Big slay",
                )
            return HttpResponseRedirect(reverse("wordlist:innsending"))
        


        if nounform.is_valid():       
            nounform_instace = nounform.save(commit=False)
            nounform_instace.author = request.user
            nounform_instace.save()
            nounform.save_m2m()

        if verbform.is_valid():       
            verbform_instace = verbform.save(commit=False)
            verbform_instace.author = request.user
            verbform_instace.save()
            verbform.save_m2m()

        if adjectiveform.is_valid():       
            adjectiveform_instace = adjectiveform.save(commit=False)
            adjectiveform_instace.author = request.user
            adjectiveform_instace.save()
            adjectiveform.save_m2m()

        if wordform.is_valid():
            wordform_instace = wordform.save(commit=False)
            wordform_instace.author = request.user
            wordform_instace.save()
            wordform.save_m2m()


            messages.add_message(
                request,
                messages.SUCCESS,
                f"Ditt ord er lagret.",
                extra_tags="Big slay",
            )
            return HttpResponseRedirect(reverse("wordlist:index"))
    else:
        checkwhatformform = CheckWhatFormForm()
        
    context = {"checkwhatformform":checkwhatformform, "wordform":wordform, "nounform":nounform, "verbform":verbform, "adjectiveform":adjectiveform} 
    return render(request, "createWord.html", context)





@permission_required("wordlist.change_word")
def adminWord(request, pk):
    word = get_object_or_404(Word, id=pk)
    wordform = WordInput(data=request.POST or None, files=request.FILES or None, instance=word)
    nounform = NounInput(data=request.POST or None, files=request.FILES or None, instance=word.noun)
    verbform = VerbInput(data=request.POST or None, files=request.FILES or None, instance=word.verb)
    adjectiveform = AdjectiveInput(data=request.POST or None, files=request.FILES or None, instance=word.adjective)
    referanse = 0

    if request.method == "POST":

        try:
            if nounform.is_valid():
                nounform_instace = nounform.save(commit = False)
                nounform_instace.save()
                referanse = 1

        except:
            try:
                if verbform.is_valid():
                    verbform_instace = verbform.save(commit = False)
                    verbform_instace.save()
                    referanse = 2
                    
            except:
                try:
                    if adjectiveform.is_valid():
                        adjectiveform_instace = adjectiveform.save(commit = False)
                        adjectiveform_instace.save()
                        referanse = 3
                        
                except:
                    try:
                        print(1)
                        nounform.save()
                    except:
                        try:
                            print(1)
                            verbform.save()
                        except:
                            try:
                                print(1)
                                adjectiveform.save()
                            except:
                                pass
        if referanse == 0:
            pass
        if referanse == 1:
            for i in range(len(Noun.objects.all())):
                if str(Noun.objects.all()[i]) == str(nounform.cleaned_data["indefinite_singular"]):
                    word.noun = Noun.objects.all()[i]
                    word.save()

        if referanse == 2:
            for i in range(len(Verb.objects.all())):
                if str(Verb.objects.all()[i]) == str(verbform.cleaned_data["infinitive"]):
                    word.noun = Noun.objects.all()[i]
                    word.save()

        if referanse == 3:
            for i in range(len(Adjective.objects.all())):
                if str(Adjective.objects.all()[i]) == str(adjectiveform.cleaned_data["positive"]):
                    word.noun = Noun.objects.all()[i]
                    word.save()

        

        
        return HttpResponseRedirect(reverse("wordlist:details", args=[pk]))
    
    context = {"wordform": wordform, "nounform":nounform, "verbform":verbform, "adjectiveform":adjectiveform}
    return render(request, "adminWord.html", context)





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

    try:
        substantiv = ordet.noun
    except:
        substantiv = ""

    try:
        verb = ordet.verb
    except:
        verb = ""

    try:
        adjektiv = ordet.adjective
    except:
        adjektiv = ""
    
    context = {"ord": ordet, "substantiv": substantiv, "verb": verb, "adjektiv": adjektiv} 
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
                extra_tags="KATEGORIEN DIN ER ENDRET"
            )
            return HttpResponseRedirect(reverse("wordlist:admincategory"))
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





def deletecategoryViews(request, pk):
    category_object = get_object_or_404(Category, id = pk)

    category_object.delete()

    messages.add_message(
        request,
        messages.SUCCESS,
        "Kategorien gikk adundas",
        extra_tags = "Slettet",
    )
    return HttpResponseRedirect(reverse("wordlist:admincategory"))


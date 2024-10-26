
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



def fsort(settet, sorteringsord): #listesortering

    filtersett = []
    enerord = []
    toerord = []
    treerord =[]
    fireerord = []

    for i in range(len(settet)):
        a =  str(settet[i][0])
        b = list(a)

        
        førstesortering = []
        andresortering = []
        tredjesortering = []
        fjerdesortering = []

        for j in range(len(b)):
            if b[j] in sorteringsord:
                førstesortering.append(b[j])
        for k in range(len(førstesortering) - 1):
                num1 = førstesortering[k] + førstesortering[k+1]
                if num1 in sorteringsord:
                    andresortering.append(num1)
                try:
                    num2 = førstesortering[k] + førstesortering[k+1] + førstesortering[k+2]
                    if num2 in sorteringsord:
                        tredjesortering.append(num2)
                    num3 = førstesortering[k] + førstesortering[k+1] + førstesortering[k+2] + førstesortering[k+3]
                    if num3 in sorteringsord:
                        fjerdesortering.append(num3)
                except:
                    pass
        if len(fjerdesortering) > 0:
            fireerord.append(settet[i])
        else: 
            if len(tredjesortering) > 0:
                treerord.append(settet[i])
            else:
                if len(andresortering) > 0:
                    toerord.append(settet[i])
                else:
                    if len(førstesortering) > 0:
                        enerord.append(settet[i])

    for i in fireerord:
        filtersett.append(i)
    for i in treerord:
        filtersett.append(i)
    for i in toerord:
        filtersett.append(i)
    for i in enerord:
        filtersett.append(i)
        
    return filtersett
                


@login_required()
def ordListe(request):

    verbs = Verb.objects.all()
    adjectives = Adjective.objects.all()
    nouns = Noun.objects.all()
    word = Word.objects.all()

    # print(verbs)
    # print(adjectives)
    # print(nouns)
    # print(word)
    # verbs = verbs.values_list('word', 'picture', 'explanations', 'category')
    # adjectives = adjectives.values_list('word', 'picture', 'explanations', 'category')
    # nouns = nouns.values_list('word', 'picture', 'explanations', 'category')
    # word = word.values_list('word', 'picture', 'explanations', 'category')
    
    # alle_ord = ((verbs.union(adjectives)).union(nouns)).union(word)

    # print(alle_ord)

    alle_ord = [] # (1 = verb, 2 = adjective, 3 = noun, 4 = word)
    for i in verbs:
        alle_ord.append((i, 1))
    for i in adjectives:
        alle_ord.append((i, 2))
    for i in nouns:
        alle_ord.append((i, 3))
    for i in word:
        alle_ord.append((i, 4))
    # print(alle_ord)
    # print(len(alle_ord))
    
    form = WordSearchMainPage()
    kategorier = Category.objects.all()
    category_form = CategorySortingMainPage()
    



    if len(alle_ord) == 0:
        return render(request, "404.html")
    else:
        form = WordSearchMainPage(request.POST or None)

        if request.method == "POST":
            if form.is_valid():                
                if request.POST["submit"] == "Søk!":
                    the_word = form.cleaned_data.get("the_word")
                    print(alle_ord)
                    alle_ord = fsort(alle_ord, the_word)
                    # alle_ord = filter(fsort, alle_ord)
                    # alle_ord = alle_ord.objects.filter(word__icontains = the_word)
                    
    if not kategorier.exists():
            return render(request, "404.html")
    else:
        category_form = CategorySortingMainPage(request.POST or None)
        if request.method == "POST":
            if category_form.is_valid():              
                if request.POST["submit"] == "Ta meg til kategorien":
                    print(alle_ord)
                    the_category = category_form.cleaned_data.get("category")
                    alle_ord_2 = []

                    instance0 = Word.objects.filter(category = the_category)
                    instance1 = Adjective.objects.filter(category = the_category)
                    instance2 = Noun.objects.filter(category = the_category)
                    instance3 = Verb.objects.filter(category = the_category)

                    for i in instance0:
                        alle_ord_2.append(i)
                    for i in instance1:
                        alle_ord_2.append(i)
                    for i in instance2:
                        alle_ord_2.append(i)
                    for i in instance3:
                        alle_ord_2.append(i)
                    
                    alle_ord_3 = []
                    for i in alle_ord:
                        if i[0] in alle_ord_2:
                            alle_ord_3.append(i)

                    alle_ord = alle_ord_3

                    


    # profile = get_object_or_404(Profile, user=request.user)
    # alle_ord_2 = []
    # if int(profile.grade) < 2:
    #     for i in alle_ord:
    #         if i[0].secret == False:
    #             alle_ord_2.append(i)
    #     alle_ord = alle_ord_2

        # alle_ord = alle_ord.filter(secret=False).order_by("word")

    # obj_per_page = 30  # Show 30 words per page.
    # if len(alle_ord) < obj_per_page:
    #     context = {"word": alle_ord, "form": form, "category": kategorier, "category_form": category_form}

    # else:
    #     paginator = Paginator(alle_ord, obj_per_page)

    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #     alle_ord = page_obj
  

    for i in alle_ord:
        i[0].explanations = i[0].explanations[:25] + "..."
    
    context = {"alle_ord": alle_ord, "form": form, "category": kategorier, "category_form": category_form}
    return render(request, "wordall.html", context)





@permission_required("wordlist.add_word")
def createWord(request):
    
    checkwhatformform = CheckWhatFormForm()
    wordform = WordInput()
    verbform = VerbInput()
    nounform = NounInput()
    adjectiveform = NounInput()
    formindex = 0

    if request.method == "POST" :
        print(request.POST,"hei")
        # print(checkwhatformform.cleaned_data)
        if request.POST['choice'] == "1":
            wordform = WordInput()
            formindex = 1
        if request.POST['choice'] == "2":
            verbform = VerbInput()
            formindex = 2
        if request.POST['choice'] == "3":
            nounform = NounInput()
            formindex = 3
        if request.POST['choice'] == "4":
            adjectiveform = AdjectiveInput()
            formindex = 4


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
        
        
    context = {"checkwhatformform":checkwhatformform, "wordform":wordform, "nounform":nounform, "verbform":verbform, "adjectiveform":adjectiveform, "formindex":formindex} 
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
def details(request, pk, klassetall): # (1 = verb, 2 = adjective, 3 = noun, 4 = word)
    
    if klassetall == 1:
        ordet = (get_object_or_404(Verb, id=pk), klassetall)
    if klassetall == 2:
        ordet = (get_object_or_404(Adjective, id=pk), klassetall)
    if klassetall == 3:
        ordet = (get_object_or_404(Noun, id=pk), klassetall)
    if klassetall == 4:
        ordet = (get_object_or_404(Word, id=pk), klassetall)


    context = {"ord": ordet} # "substantiv": substantiv, "verb": verb, "adjektiv": adjektiv
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


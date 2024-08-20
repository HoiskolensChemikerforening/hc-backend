
from .models import Word, Category, Noun, Verb, Adjective
from .forms import WordInput, WordSearchMainPage, CategorySortingMainPage, CategoryInput, NounInput, VerbInput, AdjectiveInput
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
                    
                    
   

    


    obj_per_page = 30  # Show 30 words per page.
    if len(alle_ord) < obj_per_page:
        context = {"word": alle_ord, "form": form, "category": kategorier, "category_form": category_form}

    else:
        paginator = Paginator(alle_ord, obj_per_page)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        alle_ord = page_obj


    #dette må gjøres noe med, finne en måte å gjøre det hemmelig for førsteklasse de første 2 månedene
    # print(request.user)
    # print(User.date_joined)
    #  # print(profile.grade)
    # if Profile.user.date_joined

    profile = get_object_or_404(Profile, user=request.user)
   
    # if int(profile.grade) < 2:
    #    alle_ord = alle_ord.filter(secret=False).order_by("word")

    for i in alle_ord:
        i.explanations = i.explanations[:25] + "..."
    
    context = {"word": alle_ord, "form": form, "category": kategorier, "category_form": category_form}
    return render(request, "wordall.html", context)



@permission_required("wordlist.add_word")
def createWord(request):
    if request.method == "POST":
        wordform = WordInput(data=request.POST, files=request.FILES)
        nounform = NounInput(data=request.POST, files=request.FILES)
        verbform = VerbInput(data=request.POST, files=request.FILES)
        adjectiveform = AdjectiveInput(data=request.POST, files=request.FILES)
        print("#"*30)
        print("POST-requesten:", request.POST)
        # print("Files_requesten:", request.FILES)
        
        print("#"*30)
        
        
        if "nytt" in request.POST and wordform.is_valid():
            referanse = 0
            try:
                if "nytt" in request.POST and nounform.is_valid():
                    nounform_instace = nounform.save(commit = False)
                    nounform_instace.author = request.user
                    nounform_instace.save()
                    nounform.save_m2m()
                    referanse = 1

                    
                    
                    
                    print("#"*30)
                    print("nounform.cleaned_data:", nounform.cleaned_data)
                    print("nounform.cleaned_data[indefinite_singular]:", nounform.cleaned_data["indefinite_singular"])
                    print("Noun:nounform.cleaned_data[indefinite_singular]:", {Noun:nounform.cleaned_data["indefinite_singular"]})
                    print("#"*30)
                                                                     
            except:
                try:
                    if "nytt" in request.POST and verbform.is_valid():
                        verbform_instace = verbform.save(commit = False)
                        verbform_instace.author = request.user
                        verbform_instace.save()
                        verbform.save_m2m()
                        referanse = 2
                        
                except:
                    try:
                        if "nytt" in request.POST and adjectiveform.is_valid():
                            adjectiveform_instace = adjectiveform.save(commit = False)
                            adjectiveform_instace.author = request.user
                            adjectiveform_instace.save()
                            adjectiveform.save_m2m()
                            referanse = 3
                            
                    except:
                        pass
        
            if "nytt" in request.POST and wordform.is_valid():
                wordform_instace = wordform.save(commit=False)
                wordform_instace.author = request.user
                wordform_instace.save()
                wordform.save_m2m()
                if referanse == 0:
                    pass
                if referanse == 1:
                    ordet = get_object_or_404(Word, word = wordform.cleaned_data["word"])
                    print("#"*30)
                    print("Noun.objects.all():", Noun.objects.all())
                    print("Noun.objects.all()[0]:", Noun.objects.all()[0])
                    print("Noun.objects.all()[1]:", Noun.objects.all()[1])
                    print("Noun.objects.all()[2]:", Noun.objects.all()[2])
                    print("#"*30)
                    print("nounform.cleaned_data[indefinite_singular]:", nounform.cleaned_data["indefinite_singular"])
                    for i in range(len(Noun.objects.all())):
                        print(Noun.objects.all()[i])

                        if str(Noun.objects.all()[i]) == str(nounform.cleaned_data["indefinite_singular"]):
                            ordet.noun = Noun.objects.all()[i]
                            print("#"*30)
                            print("ordet.noun:", ordet.noun)
                            print("#"*30)

                    

                    print("#"*30)
                    print("wordform:", wordform)
                    print("#"*30)
                    print(" wordform.cleaned_data:", wordform.cleaned_data)
                    print("#"*30)
                    print("ordet:", ordet)
                    print("#"*30)
                    print("ordet.noun:", ordet.noun)
                    print("#"*30)

                # wordform.cleaned_data["noun"] = {Noun:nounform.cleaned_data["indefinite_singular"]}


                
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
            wordform.save_m2m()
            


            # try:
            #     if nounform.is_valid():
            #         nounform_instace = nounform.save(commit = False)
            #         nounform_instace.author = request.user
            #         nounform_instace.save()
            #         nounform.save_m2m()
            #         pass
            # except:
            #     try:
            #         if verbform.is_valid():
            #             verbform_instace = verbform.save(commit = False)
            #             verbform_instace.author = request.user
            #             verbform_instace.save()
            #             verbform.save_m2m()
            #             pass
            #     except:
            #         try:
            #             if adjectiveform.is_valid():
            #                 adjectiveform_instace = adjectiveform.save(commit = False)
            #                 adjectiveform_instace.author = request.user
            #                 adjectiveform_instace.save()
            #                 adjectiveform.save_m2m()
            #                 pass
            #         except:
            #             pass
                    

        

        

        

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Ditt ord er lagret.",
                extra_tags="Big slay",
            )
            return HttpResponseRedirect(reverse("wordlist:index"))
    else:
        wordform = WordInput()
        nounform = NounInput()
        verbform = VerbInput()
        adjectiveform = AdjectiveInput()
    context = {"wordform":wordform, "nounform":nounform, "verbform":verbform, "adjectiveform":adjectiveform} 
    return render(request, "createWord.html", context)

@permission_required("wordlist.change_word")
def adminWord(request, pk):
    word = get_object_or_404(Word, id=pk)
    noun = Noun.objects.filter(word = word)
    verb = Verb.objects.filter(word = word)
    adjective = Adjective.objects.filter(word = word)
    


    
    # verb = get_object_or_404(Word, id=pk)
    # adjective = get_object_or_404(Word, id=pk)
    print("Dette er word:" , word)
    # print("Dette er noun:" , noun)
    # print("Dette er verb:" , verb)
    # print("Dette er adjective:" , adjective)

    nounform = {Noun: word}
    verbform = {Verb: word}
    adjectiveform = {Adjective: word}



    # wordform = WordInput(data=request.POST or None, files=request.FILES or None, instance=word)
    # nounform = NounInput(data=request.POST or None, files=request.FILES or None, instance=word)
    # verbform = VerbInput(data=request.POST or None, files=request.FILES or None, instance=word)
    # adjectiveform = AdjectiveInput(data=request.POST or None, files=request.FILES or None, instance=word)

    wordform = WordInput(data=request.POST or None, files=request.FILES or None, instance=word)
    nounform = NounInput(data=request.POST or None, files=request.FILES or None, instance=noun[0])
    verbform = VerbInput(data=request.POST or None, files=request.FILES or None, instance=verb[0])
    adjectiveform = AdjectiveInput(data=request.POST or None, files=request.FILES or None, instance=adjective[0])
    # try:
    #     nounform = NounInput(data=request.POST or None, files=request.FILES or None, instance=noun[0])
    # except: 
    #     try:
    #         verbform = VerbInput(data=request.POST or None, files=request.FILES or None, instance=verb[0])
    #     except:
    #         try:
    #             adjectiveform = AdjectiveInput(data=request.POST or None, files=request.FILES or None, instance=adjective[0])
    #         except:
    #             pass
    
    

    if request.method == "POST":
        print("wordform:")
        print(wordform)
        print("nounform:")
        print(nounform)
        print("verbform:")
        print(verbform)
        print("adjectiveform:")
        print(adjectiveform)
        print(1)

        if wordform.is_valid():
            print(2)
            wordform.save()
        print("jeg går videre")
        try:
            if nounform.is_valid():
                print(3)
                nounform.save()
        except:
            pass
        try:
            if verbform.is_valid():
                print(4)
                verbform.save()
        except:
            pass
        try:
            if adjectiveform.is_valid():
                print(5)
                adjectiveform.save()
        except:
            pass


        messages.add_message(
                request,
                messages.SUCCESS,
                "Ordet ble endret",
                extra_tags="Endret",
            )
            
        return HttpResponseRedirect(reverse("wordlist:details", args=[pk]))
    context = {"wordform": wordform,"nounform":nounform, "verbform":verbform, "adjectiveform":adjectiveform, "word":word}
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

    try:
        substantiv = ordet.noun
    except:
        substantiv = ""

    try:
        # verb = Verb.objects.get( word=ordet)
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


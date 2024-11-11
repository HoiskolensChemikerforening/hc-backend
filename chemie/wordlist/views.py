from .models import Word, Category, Noun, Verb, Adjective
from .forms import (
    WordInput,
    WordSearchMainPage,
    CategorySortingMainPage,
    CategoryInput,
    NounInput,
    VerbInput,
    AdjectiveInput,
    CheckWhatFormForm,
)
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


def fsort(settet, sorteringsord):  # listesortering
    filtersett = []
    enerord = []
    toerord = []
    treerord = []
    fireerord = []

    for i in range(len(settet)):
        a = str(settet[i][0])
        b = list(a)

        førstesortering = []
        andresortering = []
        tredjesortering = []
        fjerdesortering = []

        for j in range(len(b)):
            if b[j] in sorteringsord:
                førstesortering.append(b[j])
        for k in range(len(førstesortering) - 1):
            num1 = førstesortering[k] + førstesortering[k + 1]
            if num1 in sorteringsord:
                andresortering.append(num1)
            try:
                num2 = (
                    førstesortering[k]
                    + førstesortering[k + 1]
                    + førstesortering[k + 2]
                )
                if num2 in sorteringsord:
                    tredjesortering.append(num2)
                num3 = (
                    førstesortering[k]
                    + førstesortering[k + 1]
                    + førstesortering[k + 2]
                    + førstesortering[k + 3]
                )
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

    alle_ord = []  # (1 = verb, 2 = adjective, 3 = noun, 4 = word)
    for i in verbs:
        alle_ord.append((i, 1))
    for i in adjectives:
        alle_ord.append((i, 2))
    for i in nouns:
        alle_ord.append((i, 3))
    for i in word:
        alle_ord.append((i, 4))

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
                    alle_ord = fsort(alle_ord, the_word)

    if not kategorier.exists():
        return render(request, "404.html")
    else:
        category_form = CategorySortingMainPage(request.POST or None)
        if request.method == "POST":
            if category_form.is_valid():
                if request.POST["submit"] == "Ta meg til kategorien":
                    the_category = category_form.cleaned_data.get("category")
                    alle_ord_2 = []

                    instance0 = Word.objects.filter(category=the_category)
                    instance1 = Adjective.objects.filter(category=the_category)
                    instance2 = Noun.objects.filter(category=the_category)
                    instance3 = Verb.objects.filter(category=the_category)

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

    profile = get_object_or_404(Profile, user=request.user)

    if int(profile.grade) < 2:  # (1 = verb, 2 = adjective, 3 = noun, 4 = word)
        alle_ord_2 = []
        for i in alle_ord:
            if i[0].secret == True:
                alle_ord_2.append(i)
        for i in alle_ord_2:
            alle_ord.remove(i)

    for i in alle_ord:
        i[0].explanations = i[0].explanations[:25] + "..."

    obj_per_page = 30  # Show 30 words per page.
    if len(alle_ord) < obj_per_page:
        context = {
            "word": alle_ord,
            "form": form,
            "category": kategorier,
            "category_form": category_form,
        }

    else:
        paginator = Paginator(alle_ord, obj_per_page)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        alle_ord = page_obj

    context = {
        "alle_ord": alle_ord,
        "form": form,
        "category": kategorier,
        "category_form": category_form,
    }
    return render(request, "wordall.html", context)


@permission_required("wordlist.add_word")
def createWord(request):
    form = CheckWhatFormForm()
    formindex = 0

    if request.method == "POST" and "check" in request.POST:
        if request.POST["choice"] == "1" and "check" in request.POST:
            form = WordInput()
            formindex = 1
        if request.POST["choice"] == "2" and "check" in request.POST:
            form = VerbInput()
            formindex = 2
        if request.POST["choice"] == "3" and "check" in request.POST:
            form = NounInput()
            formindex = 3
        if request.POST["choice"] == "4" and "check" in request.POST:
            form = AdjectiveInput()
            formindex = 4

    if request.method == "POST" and "check" not in request.POST:
        print(request.POST)
        if ("nytt_tag_1" in request.POST or "tag_1" in request.POST) :
            form = WordInput(data=request.POST, files=request.FILES)
        if ("nytt_tag_2" in request.POST or "tag_2" in request.POST):
            form = VerbInput(data=request.POST, files=request.FILES)
        if ("nytt_tag_3" in request.POST or "tag_3" in request.POST):
            form = NounInput(data=request.POST, files=request.FILES)
        if ("nytt_tag_4" in request.POST or "tag_4" in request.POST):
            form = AdjectiveInput(data=request.POST, files=request.FILES)

        if "nytt_tag_3" in request.POST and form.is_valid():
            form_instace = form.save(commit=False)
            form_instace.author = request.user
            form_instace.save()
            form.save_m2m()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Ditt ord er lagret",
                extra_tags="Big slay; et nytt substantiv!",
            )
            return HttpResponseRedirect(reverse("wordlist:innsending"))

        elif "nytt_tag_2" in request.POST and form.is_valid():
            form_instace = form.save(commit=False)
            form_instace.author = request.user
            form_instace.save()
            form.save_m2m()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Ditt ord er lagret",
                extra_tags="Big slay; et nytt verb!",
            )
            return HttpResponseRedirect(reverse("wordlist:innsending"))

        elif "nytt_tag_4" in request.POST and form.is_valid():
            form_instace = form.save(commit=False)
            form_instace.author = request.user
            form_instace.save()
            form.save_m2m()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Ditt ord er lagret",
                extra_tags="Big slay; et nytt adjektiv!",
            )
            return HttpResponseRedirect(reverse("wordlist:innsending"))

        elif "nytt_tag_1" in request.POST and form.is_valid():
            form_instace = form.save(commit=False)
            form_instace.author = request.user
            form_instace.save()
            form.save_m2m()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Ditt ord er lagret",
                extra_tags="Big slay; et nytt ord!",
            )
            return HttpResponseRedirect(reverse("wordlist:innsending"))

        elif "tag_3" in request.POST and form.is_valid():
            form_instace = form.save(commit=False)
            form_instace.author = request.user
            form_instace.save()
            form.save_m2m()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Ditt ord er lagret.",
                extra_tags="Big slay; et nytt substantiv!",
            )
            return HttpResponseRedirect(reverse("wordlist:index"))

        elif "tag_2" in request.POST and form.is_valid():
            form_instace = form.save(commit=False)
            form_instace.author = request.user
            form_instace.save()
            form.save_m2m()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Ditt ord er lagret.",
                extra_tags="Big slay; et nytt verb!",
            )
            return HttpResponseRedirect(reverse("wordlist:index"))

        elif "tag_4" in request.POST and form.is_valid():
            form_instace = form.save(commit=False)
            form_instace.author = request.user
            form_instace.save()
            form.save_m2m()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Ditt ord er lagret.",
                extra_tags="Big slay; et nytt adjektiv!",
            )
            return HttpResponseRedirect(reverse("wordlist:index"))

        elif "tag_1" in request.POST and form.is_valid():
            form_instace = form.save(commit=False)
            form_instace.author = request.user
            form_instace.save()
            form.save_m2m()
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Ditt ord er lagret.",
                extra_tags="Big slay; et nytt ord!",
            )
            return HttpResponseRedirect(reverse("wordlist:index"))
        else:
            messages.add_message(
                request,
                messages.ERROR,
                f"Dette kan skyldes at orde allerede finnes i databasen, eller at forklaringen ikke er unik.",
                extra_tags="Ditt ord ble ikke lagret.",
            )

    context = {"form": form, "formindex": formindex}
    return render(request, "createWord.html", context)


@permission_required("wordlist.change_word")
def adminWord(request, pk, klassetall):
    if klassetall == 1:
        ordet = (get_object_or_404(Verb, id=pk), klassetall)
        form = VerbInput(
            data=request.POST or None,
            files=request.FILES or None,
            instance=ordet[0],
        )
    if klassetall == 2:
        ordet = (get_object_or_404(Adjective, id=pk), klassetall)
        form = AdjectiveInput(
            data=request.POST or None,
            files=request.FILES or None,
            instance=ordet[0],
        )
    if klassetall == 3:
        ordet = (get_object_or_404(Noun, id=pk), klassetall)
        form = NounInput(
            data=request.POST or None,
            files=request.FILES or None,
            instance=ordet[0],
        )
    if klassetall == 4:
        ordet = (get_object_or_404(Word, id=pk), klassetall)
        form = WordInput(
            data=request.POST or None,
            files=request.FILES or None,
            instance=ordet[0],
        )

    if request.method == "POST":
        if ordet[1] == 1 and form.is_valid():
            verbform_instace = form.save(commit=False)
            verbform_instace.save()

        if ordet[1] == 2 and form.is_valid():
            adjectiveform_instace = form.save(commit=False)
            adjectiveform_instace.save()

        if ordet[1] == 3 and form.is_valid():
            nounform_instace = form.save(commit=False)
            nounform_instace.save()

        if ordet[1] == 4 and form.is_valid():
            wordform_instace = form.save(commit=False)
            wordform_instace.save()

        return HttpResponseRedirect(
            reverse("wordlist:details", args=[pk, klassetall])
        )

    context = {"form": form}
    return render(request, "adminWord.html", context)


@permission_required("wordlist.delete_word")
def word_delete(
    request, pk, klassetall
):  # (1 = verb, 2 = adjective, 3 = noun, 4 = word)
    if klassetall == 1:
        ordet = (get_object_or_404(Verb, id=pk), klassetall)
    if klassetall == 2:
        ordet = (get_object_or_404(Adjective, id=pk), klassetall)
    if klassetall == 3:
        ordet = (get_object_or_404(Noun, id=pk), klassetall)
    if klassetall == 4:
        ordet = (get_object_or_404(Word, id=pk), klassetall)

    ordet[0].delete()
    messages.add_message(
        request, messages.SUCCESS, "Ordet ble slettet", extra_tags="Slettet"
    )
    return HttpResponseRedirect(reverse("wordlist:index"))


@login_required()
def details(
    request, pk, klassetall
):  # (1 = verb, 2 = adjective, 3 = noun, 4 = word)
    if klassetall == 1:
        ordet = (get_object_or_404(Verb, id=pk), klassetall)
    if klassetall == 2:
        ordet = (get_object_or_404(Adjective, id=pk), klassetall)
    if klassetall == 3:
        ordet = (get_object_or_404(Noun, id=pk), klassetall)
    if klassetall == 4:
        ordet = (get_object_or_404(Word, id=pk), klassetall)

    context = {"ord": ordet}
    return render(request, "details.html", context)


@permission_required("wordlist.add_word")
def admincategoryViews(request):
    categories = Category.objects.all()
    context = {"admincategory": categories}
    return render(request, "admincategory.html", context)


def editcategoryViews(request, pk):
    category = get_object_or_404(Category, id=pk)

    if request.method == "POST":
        categoryform = CategoryInput(request.POST, instance=category)
        if categoryform.is_valid():
            category_instance = categoryform.save(commit=False)
            category_instance.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                "OG FET B)",
                extra_tags="KATEGORIEN DIN ER ENDRET",
            )
            return HttpResponseRedirect(reverse("wordlist:admincategory"))
    else:
        categoryform = CategoryInput(instance=category)
    context = {"categoryform": categoryform, "category": category}
    return render(request, "editcategory.html", context)


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
                extra_tags="KATEGORIEN DIN ER LAGRET",
            )
            return HttpResponseRedirect(reverse("wordlist:admincategory"))
    else:
        categoryform = CategoryInput()
    context = {"categoryform": categoryform}
    return render(request, "createcategory.html", context)


def deletecategoryViews(request, pk):
    category_object = get_object_or_404(Category, id=pk)

    category_object.delete()

    messages.add_message(
        request,
        messages.SUCCESS,
        "Kategorien gikk adundas",
        extra_tags="Slettet",
    )
    return HttpResponseRedirect(reverse("wordlist:admincategory"))

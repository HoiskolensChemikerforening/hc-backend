from django.shortcuts import render
from .forms import RefoundForm, RefoundFormSet, AccountNumberForm
from .models import Refound


def index(request):
    accountform = AccountNumberForm()
    user = request.user
    formset = RefoundFormSet(queryset=Refound.objects.none())

    if request.POST:
        accountform = AccountNumberForm(data=request.POST)
        formset = RefoundFormSet(data=request.POST, files=request.FILES)
        print("formset", formset.is_valid())
        print("form", accountform.is_valid())
        if formset.is_valid() and accountform.is_valid():

            # Save RefoundRequest instance
            refound_request = accountform.save(commit=False)
            refound_request.user = request.user
            refound_request.save()

            # Save Receipts
            for form in formset:
                refound = form.save(commit=False)
                refound.refoundrequest = refound_request
                refound.save()


            print("valid")

    context = {
        "formset": formset,
        "accountform": accountform,
        "user": user
    }
    return render(request, "index.html", context)

def manage(request):
    pass






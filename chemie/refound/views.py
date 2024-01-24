from django.shortcuts import render, redirect
from .forms import RefoundForm, RefoundFormSet, AccountNumberForm
from .models import Refound,RefoundRequest


def index(request):
    accountform = AccountNumberForm()
    user = request.user
    formset = RefoundFormSet(queryset=Refound.objects.none())

    if request.POST:
        accountform = AccountNumberForm(data=request.POST)
        formset = RefoundFormSet(data=request.POST, files=request.FILES)
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
            return redirect("refound:myrefounds")

    context = {
        "formset": formset,
        "accountform": accountform,
        "user": user
    }
    return render(request, "index.html", context)

def my_refounds(request):
    refound_requests = RefoundRequest.objects.filter(user=request.user)
    context = {
        "refound_requests":refound_requests
    }
    return render(request, "myrefounds.html", context)


def manage(request):
    pass






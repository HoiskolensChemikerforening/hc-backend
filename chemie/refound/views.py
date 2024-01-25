from django.shortcuts import render, redirect,get_object_or_404
from .forms import RefoundForm, RefoundFormSet, AccountNumberForm
from .models import Refound,RefoundRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required()
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

@login_required()
def my_refounds(request):
    refound_requests = RefoundRequest.objects.filter(user=request.user)
    context = {
        "refound_requests":refound_requests
    }
    return render(request, "myrefounds.html", context)


@login_required()
@permission_required("refound.add_refoundrequest")
def admin_refounds(request):
    refound_requests = RefoundRequest.objects.all()
    context = {
        "refound_requests":refound_requests
    }
    return render(request, "adminrefounds.html", context)

@login_required()
def manage(request, id):
    #refound_requests = RefoundRequest.objects.all().order_by("created")
    refound = get_object_or_404(RefoundRequest, id=id)

    if not request.user.has_perm("refound.delete_refoundrequest"):
        if request.user != refound.user:
            return redirect("refound:myrefounds")

    receipts = refound.refound_set.all()
    context = {
        #"refound_requests": refound_requests,
        "refound": refound,
        "receipts": receipts,
        "status": refound.get_status()
    }
    return render(request, "detail.html", context)

@login_required()
@permission_required("refound.add_refoundrequest")
def approve_request(request, id):
    refound = get_object_or_404(RefoundRequest, id=id)
    refound.status = 3
    refound.save()
    messages.add_message(
        request,
        messages.SUCCESS,
        f"{refound.user.first_name}s søknad om {refound.get_total()} kr har blitt godkjent.",
        extra_tags="Godkjent",
    )
    return redirect("refound:detail", id=refound.id)

@login_required()
@permission_required("refound.add_refoundrequest")
def reject_request(request, id):
    refound = get_object_or_404(RefoundRequest, id=id)
    refound.status = 1
    refound.save()
    messages.add_message(
        request,
        messages.WARNING,
        f"{refound.user.first_name}s søknad om {refound.get_total()} kr har blitt avslått.",
        extra_tags="Avslått",
    )
    return redirect("refound:detail", id=refound.id)






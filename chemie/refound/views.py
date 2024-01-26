from django.shortcuts import render, redirect,get_object_or_404
from .forms import RefoundForm, RefoundFormSet, AccountNumberForm
from .models import Refound,RefoundRequest, STATUS
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum

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
    refound_requests = RefoundRequest.objects.filter(user=request.user).order_by("-created")
    context = {
        "refound_requests":refound_requests
    }
    return render(request, "myrefounds.html", context)


"""@login_required()
@permission_required("refound.add_refoundrequest")
def admin_refounds(request):
    refound_requests = RefoundRequest.objects.all().order_by("-created")
    context = {
        "refound_requests": refound_requests
    }
    return render(request, "adminrefounds.html", context)"""


def get_detail_context(request, id, admin=False):
    refound = get_object_or_404(RefoundRequest, id=id)

    if not request.user.has_perm("refound.delete_refoundrequest"):
        if request.user != refound.user:
            return redirect("refound:myrefounds")

    receipts = refound.refound_set.all()
    context = {
        # "refound_requests": refound_requests,
        "user": request.user,
        "refound": refound,
        "receipts": receipts,
        "status": refound.get_status(),
        "admin": admin
    }
    return context

@login_required()
def detail_view(request, id):
    context = get_detail_context(request, id, admin=False)
    return render(request, "detail.html", context)

@login_required()
@permission_required("refound.add_refoundrequest")
def detail_admin_view(request, id):
    context = get_detail_context(request, id, admin=True)
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


def admin_dashboard(request, annual=False, year=None):
    if annual:
        refounds = RefoundRequest.objects.filter(refound__date__year=year)
    else:
        refounds = RefoundRequest.objects.all()
    rejected = refounds.filter(status=STATUS.REJECTED).order_by("-created")
    approved = refounds.filter(status=STATUS.APPROVED).order_by("-created")
    pending = refounds.filter(status=STATUS.PENDING).order_by("-created")
    rejectsum = sum([r.get_total() for r in rejected])
    pendingsum = sum([r.get_total() for r in pending])
    approvedsum = sum([r.get_total() for r in approved])


    if len(pending) > 0 and annual:
        message = "" if len(pending) == 1 else "er"
        messages.add_message(
            request,
            messages.WARNING,
            f"{len(pending)} søknad{message} under behandling.",
            extra_tags="Warning",
        )

    context = {
        "rejected": rejected,
        "approved": approved,
        "pending": pending,
        "rejectsum": rejectsum,
        "pendingsum": pendingsum,
        "approvedsum": approvedsum,
        "year": year,
        "annual": annual
    }
    return context

@login_required()
@permission_required("refound.add_refoundrequest")
def annual_account_detail(request, year):
    context = admin_dashboard(request, annual=True, year=year)
    print(context)
    return render(request, "annual_report.html", context)

@login_required()
@permission_required("refound.add_refoundrequest")
def admin_refounds(request):
    context = admin_dashboard(request, annual=False, year=None)
    return render(request, "annual_report.html", context)






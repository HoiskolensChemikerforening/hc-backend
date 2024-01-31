from django.shortcuts import render, redirect, get_object_or_404
from .forms import RefundForm, RefundFormSet, AccountNumberForm
from .models import Refund, RefundRequest, STATUS
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum


@login_required()
def index(request):
    accountform = AccountNumberForm()
    user = request.user
    formset = RefundFormSet(queryset=Refund.objects.none())

    if request.POST:
        accountform = AccountNumberForm(data=request.POST)
        formset = RefundFormSet(data=request.POST, files=request.FILES)
        if formset.is_valid() and accountform.is_valid():

            # Save RefundRequest instance
            refund_request = accountform.save(commit=False)
            refund_request.user = request.user
            refund_request.save()

            # Save Receipts
            for form in formset:
                refund = form.save(commit=False)
                refund.refundrequest = refund_request
                refund.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f"Din søknad om {refund_request.get_total()} kr har blitt opprettet.",
                extra_tags="Suksess",
            )
            return redirect("refund:myrefunds")

    context = {"formset": formset, "accountform": accountform, "user": user}
    return render(request, "index.html", context)


@login_required()
def my_refunds(request):
    refund_requests = RefundRequest.objects.filter(
        user=request.user
    ).order_by("-created")
    context = {"refund_requests": refund_requests}
    return render(request, "myrefunds.html", context)


def get_detail_context(request, id, admin=False):
    refund = get_object_or_404(RefundRequest, id=id)

    if not request.user.has_perm("refund.delete_refundrequest"):
        if request.user != refund.user:
            return redirect("refund:myrefunds")

    receipts = refund.refund_set.all()
    context = {
        # "refund_requests": refund_requests,
        "user": request.user,
        "refund": refund,
        "receipts": receipts,
        "status": refund.get_status(),
        "admin": admin,
    }
    return context


@login_required()
def detail_view(request, id):
    context = get_detail_context(request, id, admin=False)
    return render(request, "detail.html", context)


@login_required()
@permission_required("refund.add_refundrequest")
def detail_admin_view(request, id):
    context = get_detail_context(request, id, admin=True)
    return render(request, "detail.html", context)


@login_required()
@permission_required("refund.add_refundrequest")
def approve_request(request, id):
    refund = get_object_or_404(RefundRequest, id=id)
    refund.status = 3
    refund.save()
    messages.add_message(
        request,
        messages.SUCCESS,
        f"{refund.user.first_name}s søknad om {refund.get_total()} kr har blitt godkjent.",
        extra_tags="Godkjent",
    )
    return redirect("refund:admin_refunds")


@login_required()
@permission_required("refund.add_refundrequest")
def reject_request(request, id):
    refund = get_object_or_404(RefundRequest, id=id)
    refund.status = 1
    refund.save()
    messages.add_message(
        request,
        messages.WARNING,
        f"{refund.user.first_name}s søknad om {refund.get_total()} kr har blitt avslått.",
        extra_tags="Avslått",
    )
    return redirect("refund:admin_refunds")


def reset_status(request, id):
    refund = get_object_or_404(RefundRequest, id=id)
    refund.status = 2
    refund.save()
    messages.add_message(
        request,
        messages.WARNING,
        f'Statusen på {refund.user.first_name}s søknad om {refund.get_total()} kr har blitt satt til "Under behandling".',
        extra_tags="Nullstilt",
    )
    return redirect("refund:admin_detail", id=refund.id)


def admin_dashboard(request, annual=False, year=None):
    years = None
    if annual:
        refunds = RefundRequest.get_refund_request_annual(year)
    else:
        refunds = RefundRequest.objects.all()
        years = set(
            [r.date.year for r in Refund.objects.distinct("date__year")]
        )
    rejected = refunds.filter(status=STATUS.REJECTED).order_by("-created")
    approved = refunds.filter(status=STATUS.APPROVED).order_by("-created")
    pending = refunds.filter(status=STATUS.PENDING).order_by("-created")
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
        "annual": annual,
        "years": years,
    }
    return context


@login_required()
@permission_required("refund.add_refundrequest")
def annual_account_detail(request, year):
    context = admin_dashboard(request, annual=True, year=year)
    return render(request, "annual_report.html", context)


@login_required()
@permission_required("refund.add_refundrequest")
def admin_refunds(request):
    context = admin_dashboard(request, annual=False, year=None)
    return render(request, "annual_report.html", context)


@login_required()
@permission_required("refund.add_refundrequest")
def delete_annual_report(request, year):
    refunds = RefundRequest.get_refund_request_annual(year)
    for refund in refunds:
        refund.delete()
    return redirect("refund:admin_refunds")

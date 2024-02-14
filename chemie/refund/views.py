from django.shortcuts import render, redirect, get_object_or_404
from .forms import RefundFormSet, AccountNumberForm
from .models import Refund, RefundRequest, STATUS
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from post_office import mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


@login_required()
def index(request):
    """
    View to display the index page of the refund app (refund form).
    """

    # Initialize the form asking for the account number
    accountform = AccountNumberForm()
    # Get the current user
    user = request.user
    # Initialize a formset to contain different receipts
    formset = RefundFormSet(queryset=Refund.objects.none())

    if request.POST:

        # Populate the accountform with POST data
        accountform = AccountNumberForm(data=request.POST)
        # Populate the formset with POST data and files
        formset = RefundFormSet(data=request.POST, files=request.FILES)

        # Check if formset and accountform is valid
        if formset.is_valid() and accountform.is_valid():

            # Save RefundRequest instance
            refund_request = accountform.save(commit=False)
            refund_request.user = request.user
            refund_request.save()

            # Save Receipts by iterating through all receipts in formset
            for form in formset:
                refund = form.save(commit=False)
                refund.refundrequest = refund_request
                refund.save()

            # Add success message
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Din søknad om {refund_request.get_total()} kr har blitt opprettet.",
                extra_tags="Suksess",
            )

            # Redirect to my refund page
            return redirect("refund:myrefunds")

        else:
            # Add warning message if POST data is invalid
            messages.add_message(
                request,
                messages.WARNING,
                f"Husk å fylle ut alle påkrevde felt.",
                extra_tags="Ugyldig søknad",
            )


    context = {
        "formset": formset,
        "accountform": accountform,
        "user": user
    }
    return render(request, "index.html", context)


@login_required()
def my_refunds(request):
    """
    View to display all refund requests created by the current user.
    """

    # Get all RefundRequest objects created by the current user
    refund_requests = RefundRequest.objects.filter(
        user=request.user
    ).order_by("-created")

    context = {"refund_requests": refund_requests}
    return render(request, "myrefunds.html", context)


def get_detail_context(request, id, admin=False):
    """
    Generates the context variable for the detail view pages for both normal and admin users depending on the admin variable.
    """

    # Get the refund
    refund = get_object_or_404(RefundRequest, id=id)

    # Check if a user has permissions to see the refunds
    if not request.user.has_perm("refund.delete_refundrequest"):
        if request.user != refund.user:
            return redirect("refund:myrefunds")

    # Get all receipts related to the refund request
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
    """
    Generate the detail page for a certain refund request. This view generates the page for normal users.
    """
    context = get_detail_context(request, id, admin=False)
    return render(request, "detail.html", context)


@login_required()
@permission_required("refund.add_refundrequest")
def detail_admin_view(request, id):
    """
    Generate the admin detail page for a certain refund request. This view generates the page for users with certain permissions only.
    """
    context = get_detail_context(request, id, admin=True)
    return render(request, "detail.html", context)

def error_message(request):
    # Generate fail message
    messages.add_message(
        request,
        messages.WARNING,
        f"Det har oppstått en feil.",
        extra_tags="ERROR",
    )
    return

def send_status_mail(request, refund):
    """
    Sends an e-mail to inform a user if there request has been updated.
    """
    mail_to = refund.user.email

    mail.send(
        mail_to,
        "HC <noreply@hc.ntnu.no>",
        template="refund_status",
        context={
            "amount": refund.get_total(),
            "created": refund.created.date,
            "reason": request.POST["reason"],
            "status": refund.status,
            "root_url": get_current_site(None),
        },
    )

@login_required()
@permission_required("refund.add_refundrequest")
def approve_request(request, id):
    """
    View to approve a refund request. Redirects the page to the admin refund page. Requires refoundrequest permissions.
    """
    if request.POST:
        # Get the refund request objects by id
        refund = get_object_or_404(RefundRequest, id=id)

        # Approve the refound request
        refund.status = STATUS.APPROVED
        refund.save()

        # Send info mail
        send_status_mail(request, refund)

        # Generate success message
        messages.add_message(
            request,
            messages.SUCCESS,
            f"{refund.user.first_name}s søknad om {refund.get_total()} kr har blitt godkjent.",
            extra_tags="Godkjent",
        )
    else:
        # Generate fail message if not POST
        error_message(request)
    return redirect("refund:admin_refunds")


@login_required()
@permission_required("refund.add_refundrequest")
def reject_request(request, id):
    """
    View to reject a refund request. Redirects the page to the admin refund page. Requires refoundrequest permissions.
    """
    if request.POST:
        # Get the refund request objects by id
        refund = get_object_or_404(RefundRequest, id=id)

        # Reject the refound request
        refund.status = STATUS.REJECTED
        refund.save()

        # Send info mail
        send_status_mail(request, refund)

        # Generate rejected message
        messages.add_message(
            request,
            messages.WARNING,
            f"{refund.user.first_name}s søknad om {refund.get_total()} kr har blitt avslått.",
            extra_tags="Avslått",
        )
    else:
        # Generate fail message if not POST
        error_message(request)
    return redirect("refund:admin_refunds")


@login_required()
@permission_required("refund.add_refundrequest")
def reset_status(request, id):
    """
    View to reset the status of a refund request. Redirects the page to the admin_detail page. Requires refoundrequest permissions.
    """
    if request.POST:
        # Get the refund request objects by id
        refund = get_object_or_404(RefundRequest, id=id)

        # Reset the refound request
        refund.status = STATUS.PENDING
        refund.save()

        # Send info mail
        send_status_mail(request, refund)

        # Generate reset message
        messages.add_message(
            request,
            messages.WARNING,
            f'Statusen på {refund.user.first_name}s søknad om {refund.get_total()} kr har blitt satt til "Under behandling".',
            extra_tags="Nullstilt",
        )
    else:
        # Generate fail message if not POST
        error_message(request)
    return redirect("refund:admin_detail", id=refund.id)


def admin_dashboard(request, annual=False, year=None):
    """
    Return the context for the admin dashboard.
    """

    # Initialize a variable to contain the selected year
    years = None

    if annual:
        # Get the refund requests related to the current year
        refunds = RefundRequest.get_refund_request_annual(year)
    else:
        # Get all refund request and all
        refunds = RefundRequest.objects.all()
        # Get all refund related years
        years = set(
            [r.date.year for r in Refund.objects.distinct("date__year")]
        )

    # Order request by rejected, approved and pending
    rejected = refunds.filter(status=STATUS.REJECTED).order_by("-created")
    approved = refunds.filter(status=STATUS.APPROVED).order_by("-created")
    pending = refunds.filter(status=STATUS.PENDING).order_by("-created")

    # Get the amount of rejected, approved and pending refund requests
    rejectsum = sum([r.get_total() for r in rejected])
    pendingsum = sum([r.get_total() for r in pending])
    approvedsum = sum([r.get_total() for r in approved])

    # Display warning message if there are any pending refund requests
    if len(pending) > 0 and annual:
        # Add an ending to display the plural form for multiple refund requests
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
    """
    Render the annual report page for a certain year. This pages shows all refund request objects related to a current year.
    The oldest refound date determines the year used for a refund request.
    """
    context = admin_dashboard(request, annual=True, year=year)
    return render(request, "annual_report.html", context)


@login_required()
@permission_required("refund.add_refundrequest")
def admin_refunds(request):
    """
    Render the admin dashboard displaying all refund requests.
    """
    context = admin_dashboard(request, annual=False, year=None)
    return render(request, "annual_report.html", context)


@login_required()
@permission_required("refund.add_refundrequest")
def delete_annual_report(request, year):
    """
    Render the annual report displaying all refund requests from the given year.
    """
    refunds = RefundRequest.get_refund_request_annual(year)
    for refund in refunds:
        refund.delete()
    return redirect("refund:admin_refunds")

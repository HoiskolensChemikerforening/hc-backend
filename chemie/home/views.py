from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView
from post_office import mail

from chemie.events.models import Social, Bedpres
from chemie.web_push.models import CoffeeSubmission
from chemie.home.forms import FlatpageEditForm
from chemie.news.models import Article
from chemie.sugepodden.models import Podcast
from .forms import ContactForm, PostFundsForm, PostOfficeForms
from .models import OfficeApplication


def index(request):
    all_social = Social.objects.filter(
        date__gt=timezone.now(), published=True
    ).order_by("date")
    all_bedpres = Bedpres.objects.filter(
        date__gt=timezone.now(), published=True
    ).order_by("date")
    all_posts = Article.objects.filter(published=True).order_by(
        "-published_date"
    )[:4]
    coffee = CoffeeSubmission.get_latest_submission()
    all_podcasts = Podcast.objects.filter(published=True).order_by(
        "-published_date"
    )
    latest_podcast_url = all_podcasts[0].url
    context = {
        "social": all_social,
        "bedpres": all_bedpres,
        "posts": all_posts,
        "coffee": coffee,
        "latest_podcast": latest_podcast_url,
    }
    return render(request, "chemie/index.html", context)


def contact(request):
    contact_submission = ContactForm(request.POST or None)

    if contact_submission.is_valid():
        messages.add_message(
            request,
            messages.SUCCESS,
            "Meldingen ble motatt. Takk for at du tar kontakt!",
            extra_tags="Mottatt!",
        )

        _, mail_to = zip(*settings.CONTACTS)

        mail.send(
            mail_to,
            settings.DEFAULT_FROM_EMAIL,
            template="contact_email",
            context={
                "message": contact_submission.cleaned_data.get("content"),
                "contact_name": contact_submission.cleaned_data.get(
                    "contact_name"
                ),
                "contact_email": contact_submission.cleaned_data.get(
                    "contact_email"
                ),
            },
        )
        return redirect(reverse("frontpage:home"))
    else:
        return render(
            request, "chemie/contact.html", {"form": contact_submission}
        )


def calendar(request):
    return render(request, "chemie/calendar.html")


@login_required
def request_funds(request):
    funds_form = PostFundsForm(request.POST or None, request.FILES or None)
    if funds_form.is_valid():
        instance = funds_form.save(commit=False)
        instance.author = request.user
        instance.save()
        attachments = None
        _, mail_to = zip(*settings.CONTACTS)
        mail.send(
            mail_to,
            "Webkom <webkom@hc.ntnu.no>",
            template="funds_request_form",
            context={
                "form_data": instance,
                "root_url": get_current_site(None),
            },
            attachments=attachments,
        )
        messages.add_message(
            request,
            messages.SUCCESS,
            "Din søknad er motatt og vil behandles snart.",
            extra_tags="Søknad sendt!",
        )
        return redirect(reverse("frontpage:home"))
    context = {"funds_form": funds_form}

    return render(request, "home/post_funds_form.html", context)


@login_required()
def request_office(request):
    office_form = PostOfficeForms(
        request.POST or None, initial={"student_username": ""}
    )
    author = request.user  # hente student username fra form
    already_applied = OfficeApplication.objects.filter(
        author=author,
        created__gte=timezone.now() - timezone.timedelta(days=30),
    ).exists()
    if already_applied:
        messages.add_message(
            request,
            messages.WARNING,
            "Du har allerede søkt om tilgang den siste måneden",
            extra_tags="Feil",
        )
    if office_form.is_valid():
        if already_applied:
            return redirect(reverse("frontpage:home"))
        instance = office_form.save(commit=False)
        instance.author = author
        instance.student_username = office_form.cleaned_data.get(
            "student_username"
        )
        instance.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Din søknad er motatt og vil behandles snart.",
            extra_tags="Søknad sendt!",
        )
        return redirect(reverse("frontpage:home"))

    context = {"office_form": office_form, "already_applied": already_applied}
    return render(request, "home/office_access_form.html", context)


@permission_required("flatpages.change_flatpage")
def edit_flatpage(request, url):
    if not url.startswith("/"):
        url = "/" + url
    site_id = get_current_site(request).id
    try:
        flatpage = get_object_or_404(FlatPage, url=url, sites=site_id)
    except Http404:
        if not url.endswith("/") and settings.APPEND_SLASH:
            url += "/"
            flatpage = get_object_or_404(FlatPage, url=url, sites=site_id)
        else:
            raise

    form = FlatpageEditForm(request.POST or None, instance=flatpage)

    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "{} har blitt endret!".format(flatpage.title),
                extra_tags="Supert",
            )
            return redirect(
                reverse(
                    "flatpages:django.contrib.flatpages.views.flatpage",
                    kwargs={"url": flatpage.url[1:]},
                )
            )
    context = {"flatpage": flatpage, "form": form}
    return render(request, "flatpage/edit_flatpage.html", context)


class OfficeAccessApplicationListView(PermissionRequiredMixin, ListView):
    template_name = "home/office_access_list.html"
    queryset = OfficeApplication.objects.order_by("-created")
    permission_required = "home.change_officeapplication"

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
from .forms import (
    ContactForm,
    PostFundsForm,
    PostOfficeForms,
    ApprovedTermsForm,
)
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
    latest_podcast_url = Podcast.get_latest_podcast_url()

    """
    add data script
    """

    from chemie.customprofile.models import Profile
    from django.contrib.auth.models import User

    if len(User.objects.filter(username="username")) == 0:
        username = "username"
        email = "email@email.com"
        password = "pass34wors"
        u = User.objects.create_user(username, email, password)
        u.first_name = "first_name"
        u.last_name = "last_name"
        phone_number = 99856732
        address = "address1"
        p = Profile(phone_number=phone_number, address=address, approved_terms=True)
        p.user = u
        u.save()
        p.save()
        data = [{"first_name":"Ad","last_name":"Nurcombe","email":"anurcombe0@umich.edu","phone_number":"2277184067","address":"119 Graceland Place","username":"anurcombe0","single":2,"balance":82,"specialisation":4,"grade":2},
{"first_name":"Gael","last_name":"Meneur","email":"gmeneur1@people.com.cn","phone_number":"4152736422","address":"2 Tony Plaza","username":"gmeneur1","single":2,"balance":73,"specialisation":7,"grade":3},
{"first_name":"Sigismondo","last_name":"Cardenoso","email":"scardenoso2@bandcamp.com","phone_number":"6594938101","address":"30942 Village Trail","username":"scardenoso2","single":2,"balance":82,"specialisation":2,"grade":1},
{"first_name":"Deanna","last_name":"Wafer","email":"dwafer3@xrea.com","phone_number":"6756007642","address":"2982 Di Loreto Park","username":"dwafer3","single":3,"balance":25,"specialisation":5,"grade":2},
{"first_name":"Conrad","last_name":"Biner","email":"cbiner4@etsy.com","phone_number":"7469552922","address":"2 Arkansas Alley","username":"cbiner4","single":1,"balance":51,"specialisation":2,"grade":5},
{"first_name":"Patrizius","last_name":"Emmott","email":"pemmott5@nydailynews.com","phone_number":"6608381450","address":"32 Southridge Terrace","username":"pemmott5","single":1,"balance":100,"specialisation":1,"grade":2},
{"first_name":"Tildi","last_name":"Hansana","email":"thansana6@howstuffworks.com","phone_number":"4196341911","address":"28928 Buena Vista Drive","username":"thansana6","single":1,"balance":88,"specialisation":6,"grade":6},
{"first_name":"Bria","last_name":"Durward","email":"bdurward7@multiply.com","phone_number":"2977203387","address":"0 Truax Hill","username":"bdurward7","single":1,"balance":77,"specialisation":2,"grade":6},
{"first_name":"Rorie","last_name":"Deinhard","email":"rdeinhard8@flavors.me","phone_number":"4206792699","address":"4 Cascade Road","username":"rdeinhard8","single":1,"balance":18,"specialisation":7,"grade":4},
{"first_name":"Jesselyn","last_name":"Baudains","email":"jbaudains9@tiny.cc","phone_number":"7497441223","address":"6 Sunfield Plaza","username":"jbaudains9","single":2,"balance":70,"specialisation":5,"grade":1},
{"first_name":"Sherry","last_name":"Stanion","email":"sstaniona@ucla.edu","phone_number":"6739214605","address":"7513 Prairie Rose Street","username":"sstaniona","single":1,"balance":51,"specialisation":7,"grade":5},
{"first_name":"Cristabel","last_name":"Igounet","email":"cigounetb@xrea.com","phone_number":"5331630684","address":"9568 6th Trail","username":"cigounetb","single":2,"balance":98,"specialisation":7,"grade":6},
{"first_name":"Tiena","last_name":"De la Eglise","email":"tdelaeglisec@prweb.com","phone_number":"4445332088","address":"3617 Waxwing Way","username":"tdelaeglisec","single":2,"balance":30,"specialisation":1,"grade":6},
{"first_name":"Angelica","last_name":"Bagniuk","email":"abagniukd@ucsd.edu","phone_number":"9415050571","address":"0 Ramsey Park","username":"abagniukd","single":3,"balance":35,"specialisation":4,"grade":3},
{"first_name":"Warner","last_name":"Thresher","email":"wthreshere@sciencedaily.com","phone_number":"1819769886","address":"70 Anderson Junction","username":"wthreshere","single":1,"balance":81,"specialisation":6,"grade":5},
{"first_name":"Lawrence","last_name":"Arenson","email":"larensonf@whitehouse.gov","phone_number":"8839195782","address":"8860 Cody Avenue","username":"larensonf","single":2,"balance":96,"specialisation":5,"grade":3},
{"first_name":"Ally","last_name":"Dallender","email":"adallenderg@mozilla.com","phone_number":"8609388822","address":"46078 Troy Street","username":"adallenderg","single":1,"balance":96,"specialisation":3,"grade":5},
{"first_name":"Pierette","last_name":"Preskett","email":"ppresketth@umich.edu","phone_number":"7717596056","address":"14 Mesta Plaza","username":"ppresketth","single":3,"balance":41,"specialisation":4,"grade":5},
{"first_name":"Reeva","last_name":"Lyles","email":"rlylesi@bigcartel.com","phone_number":"9049907356","address":"204 Steensland Trail","username":"rlylesi","single":1,"balance":93,"specialisation":3,"grade":1},
{"first_name":"Myrtice","last_name":"Pashenkov","email":"mpashenkovj@gravatar.com","phone_number":"6637489164","address":"44 4th Drive","username":"mpashenkovj","single":1,"balance":96,"specialisation":7,"grade":3}]
        profilelst = []
        for d in data:
            username = d["username"]
            email = d["email"]
            password = "pass34wors"
            u = User.objects.create_user(username, email, password)
            u.first_name = d["first_name"]
            u.last_name = d["last_name"]
            phone_number = int(str(d["phone_number"])[:8])
            address = d["address"]
            p = Profile(phone_number=phone_number, address=address, approved_terms=True)
            p.user = u
            p.balance = float(d["balance"])
            p.specialization = d["specialisation"]
            p.grade = d["grade"]
            p.relationship_status = d["single"]
            u.save()
            p.save()
            profilelst.append(p)

            from chemie.shitbox.models import Submission
            import datetime
            sladder = [{"sladder":"Sed ante. Vivamus tortor.","date":"03.12.2021"},
{"sladder":"Curabitur in libero ut massa volutpat convallis.","date":"03.01.2022"},
{"sladder":"Ut at dolor quis odio consequat varius. Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla.","date":"21.02.2021"},
{"sladder":"Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor.","date":"02.03.2022"},
{"sladder":"Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo. Aliquam quis turpis eget elit sodales scelerisque.","date":"21.01.2022"},
{"sladder":"Nulla tellus.","date":"07.05.2021"},
{"sladder":"Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.","date":"08.07.2022"},
{"sladder":"Curabitur gravida nisi at nibh. In hac habitasse platea dictumst.","date":"08.12.2022"},
{"sladder":"Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam. Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam.","date":"11.01.2021"},
{"sladder":"Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus. Curabitur at ipsum ac tellus semper interdum.","date":"27.09.2022"},
{"sladder":"Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.","date":"17.12.2022"},
{"sladder":"Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat.","date":"14.07.2021"},
{"sladder":"Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.","date":"13.11.2022"},
{"sladder":"Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet.","date":"05.02.2022"},
{"sladder":"Morbi vel lectus in quam fringilla rhoncus. Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis. Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus nisi eu orci. Mauris lacinia sapien quis libero. Nullam sit amet turpis elementum ligula vehicula consequat.","date":"16.12.2022"},
{"sladder":"Suspendisse ornare consequat lectus.","date":"16.06.2020"},
{"sladder":"Etiam pretium iaculis justo.","date":"06.07.2021"},
{"sladder":"Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit.","date":"19.03.2022"},
{"sladder":"Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis.","date":"07.03.2021"},
{"sladder":"Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh.","date":"23.10.2021"}]
        userlst = ['scardenoso2', 'bdurward7', 'thansana6', 'thansana6', 'sstaniona', 'adallenderg', 'wthreshere', 'tdelaeglisec', 'wthreshere', 'anurcombe0', 'scardenoso2', 'adallenderg', 'ppresketth', 'sstaniona', 'larensonf', 'larensonf', 'tdelaeglisec', 'wthreshere', 'ppresketth', 'ppresketth']
        #from django.utils import timezone
        for i, s in enumerate(sladder):
            date = timezone.datetime.strptime(s["date"], '%d.%m.%Y').date()
            print(date)
            u = User.objects.get(username=userlst[i])
            sl = Submission(content=s["sladder"], author=u)
            sl.save()
            sl.date = date
            sl.save(update_fields=['date'])
    """end"""



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
    approved_terms_form = ApprovedTermsForm(request.POST or None)
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
    if office_form.is_valid() and approved_terms_form.is_valid():
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

    context = {
        "office_form": office_form,
        "already_applied": already_applied,
        "approved_terms_form": approved_terms_form,
    }
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

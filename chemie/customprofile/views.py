from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as OldLoginView
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import ValidationError
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from urllib.parse import urlencode

from rest_framework import generics
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .email import send_forgot_password_mail
from .forms import ApprovedTermsForm
from .forms import (
    RegisterUserForm,
    RegisterProfileForm,
    EditUserForm,
    EditProfileForm,
    ForgotPassword,
    SetNewPassword,
    NameSearchForm,
    AddCardForm,
    EditPushForm,
    EndYearForm,
)
from .forms import ApprovedTermsForm
from .models import (
    UserToken,
    Profile,
    Membership,
    GRADES,
    ProfileManager,
    Medal,
    MEMBERSHIP_DURATIONS,
    SPECIALIZATION,
    RELATIONSHIP_STATUS,
    RegisterPageStatus,
)
from .serializers import (
    MedalSerializer,
    ProfileSerializer,
    CustomTokenObtainPairSerializer,
)


def register_user(request):
    page_status = RegisterPageStatus.objects.first()
    if not page_status or not page_status.is_active:
        return render(
            request, "customprofile/registration_disabled.html", status=403
        )

    user_core_form = RegisterUserForm(request.POST or None)
    user_profile_form = RegisterProfileForm(
        request.POST or None, request.FILES or None
    )
    approved_terms_form = ApprovedTermsForm(request.POST or None)
    if (
        user_core_form.is_valid()
        and user_profile_form.is_valid()
        and approved_terms_form.is_valid()
    ):
        user = user_core_form.save(commit=False)
        user.set_password(user_core_form.password_matches())
        user.save()

        profile = user_profile_form.save(commit=False)
        profile.user = user
        profile.approved_terms = True
        profile.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Brukeren din er opprettet!",
            extra_tags="Takk!",
        )
        return redirect("profile:register")
    context = {
        "user_core_form": user_core_form,
        "user_profile_form": user_profile_form,
        "approved_terms_form": approved_terms_form,
    }
    return render(request, "customprofile/register.html", context)


@login_required
def edit_profile(request):
    user = request.user
    new_password_form = PasswordChangeForm(
        user=user, data=request.POST or None
    )
    user_form = EditUserForm(request.POST or None, instance=request.user)
    try:
        current_profile = request.user.profile
    except:
        current_profile = Profile(user=user)
    profile_form = EditProfileForm(
        request.POST or None, instance=current_profile
    )
    if request.POST:
        if new_password_form.has_changed():
            # The user has filled in something in at least one field
            if new_password_form.is_valid():
                new_password_form.save()
                update_session_auth_hash(request, new_password_form.user)
                new_password_form = PasswordChangeForm(user=user, data=None)
        else:
            # Reset the password form because of the errors it throws, being empty raises errors
            new_password_form = PasswordChangeForm(user=user)
        if user_form.has_changed() or profile_form.has_changed():
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

        if not (
            user_form.errors or profile_form.errors or new_password_form.errors
        ):
            messages.add_message(
                request, messages.SUCCESS, "Dine endringer har blitt lagret!"
            )

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "change_password_form": new_password_form,
    }
    return render(request, "customprofile/editprofile.html", context)


@login_required
def edit_push(request):
    form = EditPushForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            # Sets all subscriptions to false
            user_subscriptions = request.user.profile.subscriptions.all()
            for sub in user_subscriptions:
                sub.active = False
                sub.save()

            # sets the picked subscriptions to True
            subscription_query = form.cleaned_data["subscriptions"]
            for sub in subscription_query:
                if sub in user_subscriptions:
                    user_sub = user_subscriptions.get(
                        subscription_type=sub.subscription_type
                    )
                    user_sub.active = True
                    user_sub.save()
            return redirect(reverse("customprofile:edit-push"))
    context = {"form": form}
    return render(request, "customprofile/editpush.html", context)


def forgot_password(request):
    form = ForgotPassword(request.POST or None)
    if request.POST:
        email = form.data.get("email")
        if form.is_valid():
            try:
                user = User.objects.get(email=email)
                token = UserToken.objects.create(user=user)
                send_forgot_password_mail(email, user, token)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Sjekk {} for videre detaljer".format(email),
                    extra_tags="Tilbakestille passord",
                )
                return redirect(reverse("frontpage:home"))

            except ObjectDoesNotExist:
                form.add_error(
                    None,
                    ValidationError(
                        {
                            "email": [
                                "Vi finner ingen bruker med denne e-posten"
                            ]
                        }
                    ),
                )

    context = {"form": form}
    return render(request, "customprofile/forgot_password.html", context)


def activate_password(request, code):
    try:
        activator = UserToken.objects.get(key=code)
    except ObjectDoesNotExist:
        raise Http404
    password_form = SetNewPassword(request.POST or None)
    if request.POST:
        if password_form.is_valid():
            password = password_form.data.get("password_new")
            activator.set_password(password)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Ditt passord ble endret",
                extra_tags="Suksess",
            )
            return redirect(reverse("frontpage:home"))

    context = {"form": password_form}
    return render(
        request, "customprofile/set_forgotten_password.html", context
    )


@permission_required("customprofile.change_membership")
def view_memberships(request, year=1):
    # If url arg year is invalid, make it valid.
    if year not in GRADES:
        if year > GRADES.FIFTH.value:
            year = GRADES.FIFTH.value
        else:
            year = 1

    form = NameSearchForm(request.POST or None)

    if request.method == "POST":
        # Find users from search form
        if form.is_valid():
            search_field = form.cleaned_data.get("search_field")
            users = find_user_by_name(search_field)
            profiles = Profile.objects.filter(user__in=users)
        else:
            profiles = Profile.objects.filter(
                grade=year, user__is_active=True
            ).order_by("user__last_name")

    else:
        profiles = Profile.objects.filter(
            grade=year, user__is_active=True
        ).order_by("user__last_name")

    context = {
        "profiles": profiles,
        "grades": GRADES,
        "search_form": form,
        "membership_durations": MEMBERSHIP_DURATIONS,
    }
    return render(request, "customprofile/memberships.html", context)


@permission_required("customprofile.change_membership")
def change_membership_status(request, profile_id, duration):
    person = Profile.objects.get(pk=profile_id)

    start_date = timezone.now()
    end_date = start_date + timedelta(days=duration * 365)
    endorser = request.user

    if person.membership is None:
        # Create a new membership
        membership = Membership(
            start_date=start_date, end_date=end_date, endorser=endorser
        )
        membership.save()
        person.membership = membership
        person.save()

    else:
        # Make existing membership valid again
        membership = person.membership
        membership.start_date = start_date
        membership.end_date = end_date
        membership.endorser = endorser
        membership.save()

    membership_status = person.membership.is_active()

    return JsonResponse({"membership_status": membership_status})


@login_required
def yearbook(request, klassetrinn=0, spesialisering='', sivilstatus='', digimedaljer='', search=''): # Default inputs is what will be showcased in url when no filter is active.
    klassetrinn = int(klassetrinn)
    defaulturl = [klassetrinn, spesialisering, sivilstatus, digimedaljer] #Defaulturl is used for url --- communication between view and html
    obj_per_page = 24 #Changed based on how server handles profile load amount

    # If url arg grade is invalid, make it valid.    
    if klassetrinn not in GRADES:
        if klassetrinn > GRADES.FIFTH.value:
            klassetrinn = GRADES.FIFTH.value
        if klassetrinn in (0, '0', ''): #View may be confused by html template
            klassetrinn = 0            
        else:
            klassetrinn = 1

    form = NameSearchForm(request.GET or None) 
    profiles = Profile.objects.none()

    endYearForm = EndYearForm(request.POST or None)
    qProfilesFifth = Profile.objects.filter(grade=GRADES.FIFTH)
    search_is_used = False
    search_field = ''

    if len(qProfilesFifth) > 0:
        end_year = qProfilesFifth[0].end_year - 1
    else:
        end_year = 2030  # To handle the case of 0 profiles in 5th grade
    end_years = (
        Profile.objects.filter(grade=GRADES.DONE)
        .filter(end_year__lte=end_year)
        .order_by("-end_year")
        .values_list("end_year", flat=True)
        .distinct()
    )

    if form.is_valid(): #This is for first-time search, try func in line 395 is to keep search
        search_field = form.cleaned_data.get("search_field")
        users = find_user_by_name(search_field)
        search_is_used = True
        search = search_field

    # allow GET to override path kwargs (so links like ?spesialisering=3 work)
    get_spes = request.GET.get("spesialisering")
    get_rel = request.GET.get("sivilstatus")
    get_med = request.GET.get("digimedaljer")
    get_end_year = request.GET.get("end_year")

    if get_spes not in (None, "", "None"): #Work by Copilot. If value not None, then get/keep value. | Is to keep value, line 370-376 is to make the next change in filter
        spesialisering = get_spes
    if get_rel not in (None, "", "None"):
        sivilstatus = get_rel
    if get_med not in (None, "", "None"):
        digimedaljer = get_med
    if get_end_year not in (None, "", "None"):
        try:
            end_year = int(get_end_year)
        except ValueError:
            pass
    
    # April Fools
    crush = Profile.objects.filter(grade__lt=6).order_by("?").first()
    # crush = Profile.objects.filter(user__last_name="Groening").first()

    filter_kwargs = {"user__is_active": True} #filter key word arguments baseline
    
    #If grade == 0, then it wont filter by grade. Therefore all grades will be included.
    if klassetrinn in GRADES: 
        if klassetrinn != GRADES.DONE:
            filter_kwargs["grade"] = klassetrinn
        else: #Only filter by end_year (if it is selected )
            filter_kwargs["grade"] = 6
            if endYearForm.is_valid(): #Similar to (if end_year:)
                integer_field = endYearForm.cleaned_data.get("integer_field")
                end_year = integer_field
                filter_kwargs["end_year"] = end_year

    #When choice in tuple not chosen add kwargs to filter by a specific value.
    if spesialisering not in (None, "", "None"): 
        filter_kwargs["specialization"] = spesialisering
    if sivilstatus not in (None, "", "None"):
        filter_kwargs["relationship_status"] = sivilstatus
    if digimedaljer not in (None, "", "None"):
        filter_kwargs["medals__title"] = digimedaljer

    #Append filter to profiles shown
    if search_is_used:
        profiles = Profile.objects.select_related("user").prefetch_related("medals").filter(**filter_kwargs, user__in=users).order_by("user__last_name").distinct()
    else:
        profiles = Profile.objects.select_related("user").prefetch_related("medals").filter(**filter_kwargs).order_by("grade", "user__last_name").distinct()

    url = reverse(
        "profile:yearbook-forsok1810", 
        kwargs={
            "klassetrinn": defaulturl[0], #Klassetrinn is a int value
            "spesialisering": defaulturl[1] or "",
            "sivilstatus": defaulturl[2] or "",
            "digimedaljer": defaulturl[3] or "",
        },
    )
    
    # Handle GET, to keep search (preserve the correct search form field name)
    try:
        # get the actual html name for the search field from the form
        search_param_name = form["search_field"].html_name
    except Exception:
        # fallback if form or field is missing
        search_param_name = "search"

    search = request.GET.get(search_param_name, "").strip()

    context = {
        "profiles": profiles,
        "grades": GRADES,
        "search_form": form,
        # expose a `grade` name for template use (the selected klassetrinn)
        "grade": defaulturl[0],
        "endYearForm": endYearForm,
        "end_years": end_years,
        "sluttår": end_year,
        "spec": SPECIALIZATION,
        "crush": crush,  # April fools
        "relstat": RELATIONSHIP_STATUS,
        "medals": Medal.objects.all(),
        "klassetrinn": defaulturl[0],
        "spesialisering": defaulturl[1],
        "sivilstatus": defaulturl[2],
        "digimedaljer": defaulturl[3],
        "url": url,
        "search": search,
        # expose the actual GET parameter name for search so template can append it
        "search_param_name": search_param_name,
    }

    # Show obj_per_page per page (replace your existing pagination block)
    try:
        total_count = profiles.count()
    except Exception:
        # fallback if profiles is a list
        total_count = len(profiles)

    if total_count <= obj_per_page:
        context["profiles"] = profiles
        context["is_paginated"] = False 
    else:
        paginator = Paginator(profiles, obj_per_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # put the page into context so template can both iterate and show navigation
        context["profiles"] = page_obj       # Page is iterable
        context["page_obj"] = page_obj
        context["paginator"] = paginator
        context["is_paginated"] = page_obj.has_other_pages()

        # Build a querystring prefix that preserves other GET params (except 'page') --- This is work by Copilot
        qs = request.GET.copy()
        if "page" in qs:
            qs.pop("page")
        context["page_query_prefix"] = ("?" + qs.urlencode() + "&") if qs else "?"

    return render(request, "customprofile/yearbook.html", context)


def find_user_by_name(query_name):
    qs = User.objects.all()
    for term in query_name.split():
        qs = qs.filter( 
            Q(first_name__icontains=term) | Q(last_name__icontains=term)
        )
    return qs


class LoginView(OldLoginView):
    # Få denne til å redirecte til det under
    """
    Display the login form and a "consent" form.
    If the user login is correct and consent is given: set value and
    redirect to home page
    """

    def form_valid(self, form):
        user = form.get_user()
        if user.profile.approved_terms:
            return super().form_valid(form)

        return self.approval_form_view(self.request, form)

    def approval_form_view(self, request, loginform):
        if request.method == "POST":
            if loginform.is_valid():
                user = loginform.get_user()
                termsform = ApprovedTermsForm(request.POST or None)
                if termsform.is_valid():
                    user.profile.approved_terms = True
                    user.profile.save()
                    return super().form_valid(loginform)
                else:
                    context = super().get_context_data()
                    context["termsform"] = termsform
                    context["show_popup"] = True
                    return render(request, "registration/login.html", context)


@permission_required("customprofile.can_edit_access_card")
@login_required
def add_rfid(request):
    redirect_URL = request.GET.get("redirect")
    rfid = request.GET.get("cardnr")
    form = AddCardForm(request.POST or None, initial={"access_card": rfid})
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            user = form.cleaned_data.get("user")
            try:
                profile = Profile.objects.get(user=user)
                card_nr = ProfileManager.rfid_to_em(rfid)
                profile.access_card = card_nr
                profile.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Studentkortnr ble endret",
                    extra_tags="Hurra",
                )
                if redirect_URL:
                    return redirect(redirect_URL)
                form = AddCardForm()
            except ObjectDoesNotExist:
                # Hvis en bruker ikke finnes vil koden gå hit
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Finner ingen bruker ved brukernavn {}".format(
                        user.username
                    ),
                    extra_tags="Advarsel",
                )
            except IntegrityError:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Studentkortnummeret {} er allerede registrert på en annen bruker".format(
                        card_nr
                    ),
                    extra_tags="Advarsel",
                )
            except Exception as e:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Det skjedde noe galt. {}".format(e),
                )
        return render(
            request, "customprofile/add_card.html", context={"form": form}
        )
    return render(request, "customprofile/add_card.html", context)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileListCreate(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class MedalListCreate(generics.ListCreateAPIView):
    queryset = Medal.objects.all()
    serializer_class = MedalSerializer


class MedalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medal.objects.all()
    serializer_class = MedalSerializer

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .email import queue_activation_mail, send_my_lockers_mail
from .forms import RegisterExternalLockerUserForm, MyLockersForm
from .models import Locker, LockerUser, Ownership, LockerConfirmation
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings

from post_office import mail


def view_lockers(request, page=1):
    locker_list = Locker.objects.all()
    free_lockers = Locker.objects.filter(owner__isnull=True).count()
    paginator = Paginator(locker_list, 20)

    try:
        lockers = paginator.page(page)
    except PageNotAnInteger:
        lockers = paginator.page(1)
    except EmptyPage:
        lockers = paginator.page(paginator.num_pages)

    context = {
        "lockers": lockers,
        "free_lockers": free_lockers,
    }
    return render(request, 'lockers/list.html', context)


def my_lockers(request):
    form = MyLockersForm(request.POST or None)
    if request.POST:
        email = form.data.get('email')
        if form.is_valid():
            try:
                locker_user = LockerUser.objects.get(username=email)
                lockers = locker_user.fetch_lockers()
                send_my_lockers_mail(email, lockers, locker_user)
                messages.add_message(request, messages.SUCCESS, 'Eposten ble sendt!')
                return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, 'Skapet har soleis inga skap på vevseposten',
                                     extra_tags="Bra jobba!")

    context = {
        'form': form,
    }
    return render(request, 'lockers/mineskap.html', context)


def register_locker(request, number):
    # Fetch requested locker
    locker = Locker.objects.get(number=number)
    if not locker.is_free():
        # Locker was already taken
        raise Http404
    else:
        form_data = RegisterExternalLockerUserForm(request.POST or None)
        if form_data.is_valid():
            # Check if user already exists
            user = form_data.save(commit=False)
            try:
                user = LockerUser.objects.get(username=user.username)
            except ObjectDoesNotExist:
                user.save()

            # Create a new ownership for the user
            new_ownership = Ownership(locker=locker, user=user)
            if new_ownership.reached_limit():
                raise Http404

            new_ownership.save()

            # Create confirmation link object
            confirmation_object = new_ownership.create_confirmation()

            mail.send(
                user.username,
                settings.DEFAULT_FROM_EMAIL,
                template='lockers_activate',
                context={'user': user, 'email': user.username, 'ownership': new_ownership, "request": request,
                         "confirmation": confirmation_object},
            )
            messages.add_message(request, messages.SUCCESS,
                                 'Bokskapet er nesten reservert! '
                                 'En epost har blitt sendt til deg med videre instrukser for å bekrefte epostaddressen din.',
                                 extra_tags='Boskap - reservasjon')

            return redirect(reverse('frontpage:home'))

        context = {
            "form": form_data,
        }
        return render(request, 'lockers/registrer.html', context)


def activate_ownership(request, code):
    try:
        activator = LockerConfirmation.objects.get(key=code)
        activator.activate()
    except ObjectDoesNotExist:
        raise Http404

    messages.add_message(request, messages.SUCCESS, 'Bokskapet ble aktivert og er nå ditt =D',
                         extra_tags='Fullført')

    return redirect(reverse('frontpage:home'))


@permission_required('lockers.can_delete')
def manage_lockers(request):
    lockers = Locker.objects.prefetch_related('indefinite_locker__is_confirmed__exact=True').prefetch_related(
        'indefinite_locker__user')
    context = {
        "request": request,
        "lockers": lockers
    }
    return render(request, 'lockers/administrer.html', context)


@permission_required('lockers.can_delete')
def clear_locker(request, locker_id):
    locker = get_object_or_404(Locker, pk=locker_id)
    if locker.owner:
        locker.clear()
        locker.save()

    return redirect(reverse('bokskap:administrate') + '#locker{}'.format(locker_id))
